# Spyder

- Looks like idea does work, but the model required must be 70b.
- Okay groq seems to work really good
-  Ollama looks like probably stronger model is needed, will stick to groq
- Probably can start working on streamling this


Stage 0 # Interface to define Schemas, and set of websites, depth of search

Schema : [ json-object:schema ]
Websites : [ str:urls ]
Depth of search : int:depth

Stage 1 # Scraping web content, async - > TempDir [ file.html:page ]
Schema : [ json-object:schema ]
Files : [ str:path ]

Stage 1.5: Preprocess HTML -> Cleaned HTML or Plaintext
Files: [str:cleaned_path]


Stage 2: # Extracting data - > TempDir [ file.csv:data ]
Files : [ str:path ]

Stage 2.5: Data Validation and Normalization
Files: [str:validated_csv_path]


Stage 3: # Adding to database ( optional )

