/* sentiment_analysis.pig
   Loads a file of tweets tagged with #unitedairlines and a 
   dictionary of known sentiment words and computes a sentiment score
*/

tweets = LOAD 's3://piggyinputs/united_airlines_tweets.tsv' USING PigStorage('\t') 
    AS (id_str:chararray, tweet_url:chararray, created_at:chararray, 
        text:chararray, lang:chararray, retweet_count:int, favorite_count:int, 
        screen_name:chararray);
dictionary = LOAD 's3://piggyinputs/dictionary.tsv' USING PigStorage('\t') 
    AS (word:chararray, score:int);
english_tweets = FILTER tweets BY lang == 'en';
tokenized = FOREACH english_tweets GENERATE id_str, 
    FLATTEN( TOKENIZE(text) ) AS word;
clean_tokens = FOREACH tokenized GENERATE id_str, 
    LOWER(REGEX_EXTRACT(word, '[#@]{0,1}(.*)', 1)) AS word;
token_sentiment = JOIN clean_tokens BY word, dictionary BY word;
sentiment_group = GROUP token_sentiment BY id_str;
sentiment_score = FOREACH sentiment_group 
    GENERATE group AS id, SUM(token_sentiment.score) AS final;
classified = FOREACH sentiment_score 
    GENERATE id, ( (final >= 0)? 'POSITIVE' : 'NEGATIVE' ) AS classification, 
    final AS score;
final = ORDER classified BY score DESC;
STORE final INTO 'sentiment_analysis';
