# Resume Keyword Extraction

## Motivation
In today's competitive job market, effectively showcasing skills and experiences in a resume is crucial. Employers often use automated systems to scan resumes for specific keywords relevant to job descriptions. This tool aims to streamline the process of keyword extraction from resumes, helping job seekers identify and emphasize essential skills and qualifications to enhance their chances of being noticed by potential employers.

## About
This project is a Flask web application that utilizes Natural Language Processing (NLP) techniques to extract keywords from resumes. It employs the TF-IDF (Term Frequency-Inverse Document Frequency) method to assess the importance of words in a document, filtering out common stop words and irrelevant terms. Users can upload their resumes, and the application will process the text, returning a list of the most significant keywords.

## Features
Resume Upload: Users can upload their resumes in text format.
Keyword Extraction: Extracts and ranks keywords based on their importance.
Customizable Stop Words: Includes a set of custom stop words to refine the extraction process.
Search Functionality: Users can search for specific keywords within the extracted list.

## Uses
Job Seekers: Helps individuals tailor their resumes to include relevant keywords that align with job descriptions, increasing the chances of passing through Applicant Tracking Systems (ATS).
Recruiters: Assists recruiters in identifying key skills and qualifications from resumes quickly.
NLP Enthusiasts: A practical example for those interested in exploring text processing and keyword extraction using Python and Flask.
