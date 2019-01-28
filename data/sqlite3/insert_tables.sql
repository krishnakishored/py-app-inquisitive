/*
 * SQLite INSERT TABLE examples.
 * 
 */

INSERT INTO conjunction  SELECT id,german_word,english_word,partsofspeech FROM master WHERE partsofspeech='conjunction';
INSERT INTO noun  SELECT id,german_word,english_word,partsofspeech FROM master WHERE partsofspeech='noun';
INSERT INTO verb  SELECT id,german_word,english_word,partsofspeech FROM master WHERE partsofspeech='verb';

INSERT INTO sentence  SELECT id,german_word,english_word,partsofspeech FROM master WHERE partsofspeech='sentence';

