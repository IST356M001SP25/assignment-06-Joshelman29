import streamlit as st
import pandas as pd
import requests
import json 
from apicalls import get_google_place_details, get_azure_sentiment, get_azure_named_entity_recognition


PLACE_IDS_SOURCE_FILE = "code/solutions/cache/place_ids.csv"
CACHE_REVIEWS_FILE = "code/solutions/cache/reviews.csv"
CACHE_SENTIMENT_FILE = "code/solutions/cache/reviews_sentiment_by_sentence.csv"
CACHE_ENTITIES_FILE = "code/solutions/cache/reviews_sentiment_by_sentence_with_entities.csv"


def reviews_step(place_ids: str | pd.DataFrame) -> pd.DataFrame:
    '''
      1. place_ids --> reviews_step --> reviews: place_id, name (of place), author_name, rating, text 
    '''

    # Load input if a file path is provided
    input_df = pd.read_csv(place_ids) if isinstance(place_ids, str) else place_ids

    # Collect review data from Google Place API
    details_list = []
    for _, entry in input_df.iterrows():
        result = get_google_place_details(entry['Google Place ID'])
        details_list.append(result['result'])

    # Flatten and extract reviews
    all_reviews_df = pd.json_normalize(details_list, record_path='reviews', meta=['place_id', 'name'])

    # Select relevant fields
    final_reviews = all_reviews_df[['place_id', 'name', 'author_name', 'rating', 'text']]

    # Save to disk
    final_reviews.to_csv(CACHE_REVIEWS_FILE, index=False)
    return final_reviews


def sentiment_step(reviews: str | pd.DataFrame) -> pd.DataFrame:
    '''
      2. reviews --> sentiment_step --> review_sentiment_by_sentence
    '''

    # Load data if file path given
    reviews_data = pd.read_csv(reviews) if isinstance(reviews, str) else reviews

    # Analyze sentiment for each review
    sentiment_output = []
    for _, row in reviews_data.iterrows():
        sentiment_result = get_azure_sentiment(row['text'])
        analysis = sentiment_result['results']['documents'][0]
        for key in ['place_id', 'name', 'author_name', 'rating']:
            analysis[key] = row[key]
        sentiment_output.append(analysis)

    # Flatten sentence-level sentiment
    processed_df = pd.json_normalize(sentiment_output, record_path='sentences',
                                     meta=['place_id', 'name', 'author_name', 'rating'])

    # Rename columns
    processed_df.rename(columns={
        'text': 'sentence_text',
        'sentiment': 'sentence_sentiment'
    }, inplace=True)

    # Select key output fields
    result_df = processed_df[[
        'place_id', 'name', 'author_name', 'rating',
        'sentence_text', 'sentence_sentiment',
        'confidenceScores.positive', 'confidenceScores.neutral', 'confidenceScores.negative'
    ]]

    # Write to cache and return
    result_df.to_csv(CACHE_SENTIMENT_FILE, index=False)
    return result_df


def entity_extraction_step(sentiment: str | pd.DataFrame) -> pd.DataFrame:
    '''
      3. review_sentiment_by_sentence --> entity_extraction_step --> review_sentiment_entities_by_sentence
    '''

    # Load data from file if path is provided
    sentiment_data = pd.read_csv(sentiment) if isinstance(sentiment, str) else sentiment

    # Extract entities from each sentence
    all_entities = []
    for _, row in sentiment_data.iterrows():
        entity_response = get_azure_named_entity_recognition(row['sentence_text'])
        doc_result = entity_response['results']['documents'][0]
        for field in sentiment_data.columns:
            doc_result[field] = row[field]
        all_entities.append(doc_result)

    # Flatten entity-level results
    flat_entities = pd.json_normalize(all_entities, record_path='entities', meta=list(sentiment_data.columns))

    # Rename for clarity
    flat_entities.rename(columns={
        'text': 'entity_text',
        'category': 'entity_category',
        'subcategory': 'entity_subcategory',
        'confidenceScore': 'confidenceScores.entity'
    }, inplace=True)

    # Keep only relevant columns
    final_entities_df = flat_entities[[
        'place_id', 'name', 'author_name', 'rating',
        'sentence_text', 'sentence_sentiment',
        'confidenceScores.positive', 'confidenceScores.neutral', 'confidenceScores.negative',
        'entity_text', 'entity_category', 'entity_subcategory', 'confidenceScores.entity'
    ]]

    # Cache and return
    final_entities_df.to_csv(CACHE_ENTITIES_FILE, index=False)
    return final_entities_df


import streamlit as st # helpful for debugging as you can view your dataframes and json outputs

reviews_step(PLACE_IDS_SOURCE_FILE)
sentiment_step(CACHE_REVIEWS_FILE)
entities_df = entity_extraction_step(CACHE_SENTIMENT_FILE)
st.write(entities_df)