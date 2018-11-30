""" Uses the scripts contained within explorer.py to generate training and test data."""

import pandas as pd
import numpy as np
from knowledgestore import ks
import explorer
from multiprocessing import Pool
import copy
from logging import log

all_article_uris = explorer.all_article_uris


def main():
	data = generate_data_for_articles([all_article_uris.loc[i]["article"] for i in range(2)])
	data.to_csv("test_data.csv")
	print(data.head())
	print(data.describe())
	print("----------"")
	print(data["classification"].value_counts())
	# generate_data_chunks(star_index, end_index)


def generate_data_for_articles(articles):
	data = pd.DataFrame()
	for article_uri in articles:
		triples = explorer.generate_triples_from_uri(article_uri)
		article_text = ks.run_files_query(article_uri)
		splits_at = get_positions_of_char_in_text(" ", article_text)
		words_by_position = [(splits_at[x] + 1, splits_at[x + 1]) for x in range(len(splits_at) - 1)]
		for triple in triples:
			tdata = generate_classification_data(triple[0], triple[2], triple[1], article_uri, words_by_position)
			data = data.append(tdata,ignore_index=True)
	return data


def generate_data_chunks(start_index, end_index):
	pass


def generate_classification_data(agent, patient, correct_relations, article_uri, words_by_position):
	result_frame = pd.DataFrame()
	for word_by_position in words_by_position:
		classification = word_by_position in correct_relations
		word_row = pd.DataFrame({"agent": agent[1], "patient": patient[1], "word_start_char": word_by_position[0], "word_end_char": word_by_position[1], "classification": classification, "article_uri": article_uri}, index=[0])
		result_frame = result_frame.append(word_row, ignore_index=True)
	return result_frame


def get_positions_of_char_in_text(sought_char, text):
	return [pos for pos, char in enumerate(text) if char == sought_char]


if __name__ == "__main__":
	main()
