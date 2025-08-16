
# Visual Memory Search - System Architecture

## System Overview Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           VISUAL MEMORY SEARCH SYSTEM                          │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────────────┐  │
│  │   File Upload   │    │  Processing UI   │    │     Search Interface       │  │
│  │   Interface     │    │                  │    │                             │  │
│  │                 │    │  ┌─Progress Bar─┐ │    │  ┌─Query Input──────────┐   │  │
│  │  ┌─Drag & Drop─┐ │    │  ├─Status Text─┤ │    │  ├─Search Options──────┤   │  │
│  │  ├─File Select┤ │    │  └─File Counter─┘ │    │  └─Results Display─────┘   │  │
│  │  └─Validation──┘ │    │                  │    │                             │  │
│  └─────────────────┘    └──────────────────┘    └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                             MAIN APPLICATION                                   │
│                                 (app.py)                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─Session Management─┐  ┌─File Processing Pipeline─┐  ┌─Search Coordination─┐   │
│  │                    │  │                          │  │                     │   │
│  │ • processed_data   │  │ 1. Image Validation      │  │ • Query Analysis    │   │
│  │ • search_index     │  │ 2. OCR Text Extraction   │  │ • Multi-modal Search│   │
│  │ • processing_state │  │ 3. Visual Analysis       │  │ • Result Ranking    │   │
│  │ • UI State         │  │ 4. Thumbnail Creation    │  │ • Display Logic     │   │
│  └────────────────────┘  └──────────────────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                             PROCESSING LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ ImageProcessor  │  │  OpenAIClient   │  │  GeminiClient   │  │SearchEngine │ │
│  │                 │  │                 │  │                 │  │             │ │
│  │ ┌─OCR Methods─┐  │  │ ┌─Vision API──┐ │  │ ┌─Vision API──┐ │  │ ┌─TF-IDF───┐ │ │
│  │ ├─Ultra Fast──┤  │  │ ├─GPT-4o──────┤ │  │ ├─Gemini Flash┤ │  │ ├─Indexing─┤ │ │
│  │ ├─Balanced────┤  │  │ ├─Screenshot──┤ │  │ ├─Screenshot──┤ │  │ ├─Similarity┤ │ │
│  │ ├─Detailed────┤  │  │ │  Analysis   │ │  │ │  Analysis   │ │  │ ├─Ranking──┤ │ │
│  │ └─Basic Local─┘  │  │ └─Query Intent┘ │  │ └─Fast Process┘ │  │ └─Scoring──┘ │ │
│  │                 │  │                 │  │                 │  │             │ │
│  │ ┌─Image Prep──┐  │  │ ┌─API Config──┐ │  │ ┌─API Config──┐ │  │ ┌─Results──┐ │ │
│  │ ├─Preprocessing┤  │  │ ├─Error Handle┤ │  │ ├─Error Handle┤ │  │ ├─Filtering┤ │ │
│  │ ├─Thumbnails──┤  │  │ ├─Rate Limits─┤ │  │ ├─Rate Limits─┤ │  │ ├─Reasoning┤ │ │
│  │ └─Base64 Conv─┘  │  │ └─Response Fmt┘ │  │ └─Response Fmt┘ │  │ └─Confidence┘ │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐                    ┌─────────────────────────────────────┐  │
│  │  DataManager    │                    │          Storage Systems            │  │
│  │                 │                    │                                     │  │
│  │ ┌─Session Data─┐ │◄──────────────────►│  ┌─Session State (Streamlit)────┐   │  │
│  │ ├─Data Export──┤ │                    │  ├─processed_data (DataFrame)───┤   │  │
│  │ ├─Summaries────┤ │                    │  ├─search_index (TF-IDF Matrix)─┤   │  │
│  │ ├─Metadata─────┤ │                    │  ├─thumbnails (Base64)──────────┤   │  │
│  │ └─Cleanup──────┘ │                    │  └─processing_state─────────────┘   │  │
│  └─────────────────┘                    └─────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           EXTERNAL SERVICES                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Tesseract     │  │   OpenAI API    │  │   Google AI     │  │   System    │ │
│  │      OCR        │  │                 │  │   (Gemini)      │  │ Libraries   │ │
│  │                 │  │ • GPT-4o Vision │  │                 │  │             │ │
│  │ • Text Extract  │  │ • Image Analysis│  │ • Gemini Flash  │  │ • OpenCV    │ │
│  │ • Multi-Config  │  │ • Query Intent  │  │ • Fast Vision   │  │ • PIL/Pillow│ │
│  │ • Preprocessing │  │ • Rate Limiting │  │ • Cost Effective│  │ • scikit-learn│ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Component Flow Diagrams

### 1. File Processing Pipeline

```
Upload Files
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    IMAGE VALIDATION                            │
│  ┌─File Format Check─┐  ┌─Size Validation─┐  ┌─Corruption Check─┐ │
│  │  • PNG, JPG       │  │  • Min: 50x50   │  │  • PIL Load     │ │
│  │  • JPEG, WebP     │  │  • Max: Any     │  │  • Error Handle │ │
│  │  │  HEIC          │  │  • File Size    │  │  • Skip Invalid │ │
│  └───────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PROCESSING MODE SELECTION                    │
│                                                                 │
│  ┌─Ultra Fast─┐  ┌─Balanced──┐  ┌─Detailed OpenAI─┐  ┌─Detailed Gemini─┐
│  │ OCR Only   │  │ OCR +     │  │ OCR + OpenAI    │  │ OCR + Gemini    │
│  │ Minimal    │  │ Basic     │  │ Vision Analysis │  │ Vision Analysis │
│  │ Processing │  │ Analysis  │  │ (GPT-4o)        │  │ (Flash)         │
│  └────────────┘  └───────────┘  └─────────────────┘  └─────────────────┘
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PARALLEL PROCESSING                         │
│                                                                 │
│  ┌─────────────────┐              ┌─────────────────────────────┐ │
│  │   OCR BRANCH    │              │      VISUAL BRANCH          │ │
│  │                 │              │                             │ │
│  │  Image Input    │              │      Image Input            │ │
│  │      │          │              │          │                  │ │
│  │      ▼          │              │          ▼                  │ │
│  │ ┌─Preprocessing─┐│              │ ┌─AI Service Selection────┐ │ │
│  │ │• Grayscale    ││              │ │ • OpenAI GPT-4o        │ │ │
│  │ │• Denoise      ││              │ │ • Google Gemini Flash  │ │ │
│  │ │• Contrast     ││              │ │ • Basic Local Analysis │ │ │
│  │ │• Enhancement  ││              │ └────────────────────────┘ │ │
│  │ └───────────────┘│              │          │                  │ │
│  │      │          │              │          ▼                  │ │
│  │      ▼          │              │ ┌─Visual Description─────┐   │ │
│  │ ┌─Tesseract OCR─┐│              │ │ • UI Elements         │   │ │
│  │ │• Custom Config││              │ │ • Color Schemes       │   │ │
│  │ │• Text Extract ││              │ │ • Layout Analysis     │   │ │
│  │ │• Noise Filter ││              │ │ • Interactive Elements│   │ │
│  │ └───────────────┘│              │ └───────────────────────┘   │ │
│  │      │          │              │          │                  │ │
│  │      ▼          │              │          ▼                  │ │
│  │ ┌─Text Cleanup──┐│              │    Description Text         │ │
│  │ │• Remove Noise ││              │                             │ │
│  │ │• Normalize    ││              │                             │ │
│  │ │• Filter Short ││              │                             │ │
│  │ └───────────────┘│              │                             │ │
│  └─────────────────┘              └─────────────────────────────┘ │
│           │                                     │                 │
└───────────┼─────────────────────────────────────┼─────────────────┘
            │                                     │
            ▼                                     ▼
┌───────────────────────────────────────────────────────────────────┐
│                     DATA AGGREGATION                             │
│                                                                   │
│  ┌─Combine Results─┐  ┌─Generate Thumbnails─┐  ┌─Create Metadata─┐ │
│  │ • OCR Text      │  │ • Resize Image      │  │ • Filename      │ │
│  │ • Visual Desc   │  │ • Maintain Aspect   │  │ • Dimensions    │ │
│  │ • Confidence    │  │ • Base64 Encode     │  │ • File Size     │ │
│  │ • Timestamps    │  │ • Error Handling    │  │ • Timestamp     │ │
│  └─────────────────┘  └─────────────────────┘  └─────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
            │
            ▼
┌───────────────────────────────────────────────────────────────────┐
│                    STORAGE & INDEXING                            │
│                                                                   │
│  ┌─DataFrame Creation─┐     ┌─Search Index Build─┐                 │
│  │ • Structured Data  │────►│ • TF-IDF Matrix    │                │
│  │ • Session Storage  │     │ • Feature Vectors  │                │
│  │ • Progress Update  │     │ • Similarity Prep  │                │
│  └────────────────────┘     └────────────────────┘                │
└───────────────────────────────────────────────────────────────────┘
```

### 2. Search Operation Flow

```
User Query Input
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    QUERY PREPROCESSING                         │
│                                                                 │
│  ┌─Clean Query─┐  ┌─Search Mode─┐  ┌─Parameters─┐               │
│  │ • Normalize │  │ • Combined  │  │ • Max Results: 1-10      │ │
│  │ • Remove    │  │ • Text Only │  │ • Confidence Threshold   │ │
│  │   Special   │  │ • Visual    │  │ • Ranking Algorithm      │ │
│  │   Characters│  │   Only      │  │                          │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SIMILARITY CALCULATION                        │
│                                                                 │
│  ┌─TF-IDF Vectorization─┐              ┌─Cosine Similarity──┐    │
│  │                      │              │                    │    │
│  │  Query Vector        │              │  Query vs Content │    │
│  │      │               │              │         │          │    │
│  │      ▼               │              │         ▼          │    │
│  │ ┌─Feature Extract─┐  │     ┌───────►│ ┌─Similarity Matrix─┐  │ │
│  │ │ • N-grams       │  │     │        │ │ • Score per Doc   │  │ │
│  │ │ • Stop Words    │  │     │        │ │ • Range: 0.0-1.0  │  │ │
│  │ │ • Term Freq     │  │     │        │ │ • Higher = Better │  │ │
│  │ └─────────────────┘  │     │        │ └───────────────────┘  │ │
│  │      │               │     │        │                        │ │
│  │      ▼               │     │        └────────────────────────┘ │
│  │ ┌─Match Against─────┐ │     │                                  │
│  │ │ • OCR Text        │ │─────┘                                  │
│  │ │ • Visual Desc     │ │                                        │
│  │ │ • Combined Content│ │                                        │
│  │ └───────────────────┘ │                                        │
│  └──────────────────────┘                                        │
└─────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│                     RESULT RANKING                             │
│                                                                 │
│  ┌─Score Normalization─┐  ┌─Confidence Calc─┐  ┌─Match Reason─┐  │
│  │                     │  │                 │  │              │  │
│  │  Raw Similarity     │  │  Normalized     │  │  Explanation │  │
│  │      │              │  │      │          │  │      │       │  │
│  │      ▼              │  │      ▼          │  │      ▼       │  │
│  │ ┌─Max Score Find─┐  │  │ ┌─Percentage──┐ │  │ ┌─Word Match─┐ │ │
│  │ │ • Find Peak     │  │  │ │ (Score/Max) │ │  │ │ • Text     │ │ │
│  │ │ • Avoid Zero    │  │  │ │ * 100       │ │  │ │   Matches  │ │ │
│  │ │ • Handle Edge   │  │  │ │ = 0-100%    │ │  │ │ • Visual   │ │ │
│  │ │   Cases         │  │  │ └─────────────┘ │  │ │   Matches  │ │ │
│  │ └─────────────────┘  │  │                 │  │ │ • Semantic │ │ │
│  │      │              │  │                 │  │ │   Similar  │ │ │
│  │      ▼              │  │                 │  │ └───────────┘ │ │
│  │ ┌─Sort Descending─┐ │  │                 │  │              │ │
│  │ │ • Best First    │ │  │                 │  │              │ │
│  │ │ • Apply Limit   │ │  │                 │  │              │ │
│  │ │ • Filter Low    │ │  │                 │  │              │ │
│  │ └─────────────────┘ │  │                 │  │              │ │
│  └─────────────────────┘  └─────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RESULT FORMATTING                           │
│                                                                 │
│  ┌─Result Assembly─┐    ┌─Thumbnail Loading─┐   ┌─UI Display─┐   │
│  │                 │    │                   │   │            │   │
│  │ • Filename      │    │ • Base64 Decode   │   │ • Cards    │   │
│  │ • Confidence    │    │ • Image Recovery  │   │ • Expand   │   │
│  │ • Match Reason  │    │ • Error Handling  │   │ • Preview  │   │
│  │ • Content Prev  │    │ • Fallback Image  │   │ • Metadata │   │
│  │ • Metadata      │    │                   │   │            │   │
│  └─────────────────┘    └───────────────────┘   └────────────┘   │
└─────────────────────────────────────────────────────────────────┘
     │
     ▼
Display to User
```

### 3. Data Management Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    SESSION LIFECYCLE                           │
│                                                                 │
│  App Start                                                      │
│     │                                                           │
│     ▼                                                           │
│  ┌─Initialize Session State─┐                                   │
│  │ • processed_data = []     │                                   │
│  │ • search_index = None     │                                   │
│  │ • processing_complete = F │                                   │
│  └───────────────────────────┘                                   │
│     │                                                           │
│     ▼                                                           │
│  ┌─File Processing─────────┐                                    │
│  │ • Update progress       │                                    │
│  │ • Store in session      │                                    │
│  │ • Build search index    │                                    │
│  │ • Set complete flag     │                                    │
│  └─────────────────────────┘                                    │
│     │                                                           │
│     ▼                                                           │
│  ┌─Search Operations──────┐                                     │
│  │ • Query processing     │                                     │
│  │ • Result generation    │                                     │
│  │ • Export capabilities  │                                     │
│  └────────────────────────┘                                     │
│     │                                                           │
│     ▼                                                           │
│  ┌─Session Cleanup────────┐                                     │
│  │ • Clear data option    │                                     │
│  │ • Memory management    │                                     │
│  │ • Reset to initial     │                                     │
│  └────────────────────────┘                                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    DATA STRUCTURES                             │
│                                                                 │
│  ┌─DataFrame Schema (processed_data)─────────────────────────┐   │
│  │                                                           │   │
│  │  filename:           str    # Original file name         │   │
│  │  file_size:          int    # File size in bytes         │   │
│  │  image_dimensions:   str    # "WxH" format               │   │
│  │  ocr_text:          str    # Extracted text content      │   │
│  │  visual_description: str    # AI-generated description   │   │
│  │  thumbnail_b64:     str    # Base64 encoded thumbnail    │   │
│  │  processed_timestamp: datetime # Processing time         │   │
│  │                                                           │   │
│  │  # Added during search:                                  │   │
│  │  similarity_score:   float  # Cosine similarity         │   │
│  │  confidence_score:   float  # 0-100% confidence         │   │
│  │  match_reason:      str    # Explanation of match       │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─Search Index Schema──────────────────────────────────────┐    │
│  │                                                          │    │
│  │  tfidf_matrix:      scipy.sparse.matrix # Feature vecs  │    │
│  │  tfidf_vectorizer:  TfidfVectorizer     # Fitted model  │    │
│  │  combined_content:  list[str]           # Text corpus   │    │
│  │  feature_names:     array               # Feature terms │    │
│  └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Error Handling and Recovery

```
┌─────────────────────────────────────────────────────────────────┐
│                    ERROR HANDLING STRATEGY                     │
│                                                                 │
│  ┌─File Processing Errors─┐                                     │
│  │                        │                                     │
│  │  Invalid Format        │                                     │
│  │      │                 │                                     │
│  │      ▼                 │                                     │
│  │  ┌─Skip & Continue──┐   │     ┌─OCR Errors─────────────┐     │
│  │  │ • Log Warning    │   │     │                        │     │
│  │  │ • Show User Msg  │   │     │  Tesseract Failure     │     │
│  │  │ • Process Others │   │     │      │                 │     │
│  │  └──────────────────┘   │     │      ▼                 │     │
│  │                        │     │  ┌─Return Empty Text─┐  │     │
│  │  Corrupted Image       │     │  │ • Log Warning     │  │     │
│  │      │                 │     │  │ • Continue Process│  │     │
│  │      ▼                 │     │  │ • Fallback Mode   │  │     │
│  │  ┌─Skip & Continue──┐   │     │  └───────────────────┘  │     │
│  │  │ • Error Message  │   │     │                        │     │
│  │  │ • Process Valid  │   │     └────────────────────────┘     │
│  │  └──────────────────┘   │                                     │
│  └────────────────────────┘                                     │
│                                                                 │
│  ┌─AI Service Errors─────┐         ┌─Search Errors──────────┐   │
│  │                       │         │                       │   │
│  │  API Key Missing      │         │  Empty Results        │   │
│  │      │                │         │      │                │   │
│  │      ▼                │         │      ▼                │   │
│  │  ┌─Show Error & Stop─┐ │         │  ┌─Show No Results─┐  │   │
│  │  │ • Clear Message   │ │         │  │ • Suggest Tips  │  │   │
│  │  │ • Stop Processing │ │         │  │ • Query Examples│  │   │
│  │  └───────────────────┘ │         │  └─────────────────┘  │   │
│  │                       │         │                       │   │
│  │  Rate Limit Hit       │         │  Index Build Fail    │   │
│  │      │                │         │      │                │   │
│  │      ▼                │         │      ▼                │   │
│  │  ┌─Fallback Mode───┐  │         │  ┌─Basic Search──────┐ │   │
│  │  │ • Use Basic     │  │         │  │ • Simple String  │ │   │
│  │  │   Analysis      │  │         │  │   Matching       │ │   │
│  │  │ • Continue Proc │  │         │  │ • Reduced Feats  │ │   │
│  │  └─────────────────┘  │         │  └───────────────────┘ │   │
│  └───────────────────────┘         └───────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

This architecture diagram shows how the Visual Memory Search application components interact, from the user interface down to the external services, with detailed flow charts for the main operations: file processing, search operations, data management, and error handling.
