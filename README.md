# GLOBAL PROTEST EVENTS ANALYSIS (1990 - 2020)
![WhatsApp Image 2024-08-07 at 15 07 10_b20b0102](https://github.com/user-attachments/assets/cebf17e6-05a3-4984-b85e-09ed490f6d5c)
## Overview
This repository contains an in-depth analysis of global protest events from 1990 to 2020, aimed at understanding the underlying factors, geographical and temporal trends, patterns, and state responses. Additionally, the repository includes sentiment analysis of protest notes and tweets to provide insights into public sentiment surrounding these events.
## Notebooks included
1. #### Cleaned data:
   - **Purpose**: Data cleaning and preprocessing for the global protest dataset.
   - **Key Actions:**
   - Handled missing values.
   - Filtered data to the relevant period (1990 - 2020).
   - Applied one-hot encoding to categorical variables.
   - Dropped unnecessary columns for streamlined analysis.
2. #### Exploratory Data Analysis (EDA)
   - **Purpose:** Exploratory Data Analysis (EDA) on the cleaned protest dataset.
   - **Key Actions:**
     - Generated geographical and temporal visualizations.
     - Analyzed protest characteristics and scale.
     - Investigated state responses to protests.
       
    https://public.tableau.com/shared/2QWZQCS3H?:display_count=y&:origin=viz_share_link&:embed=y

   **The above world map shows the geographical distribution of protests.**

   ![image](https://github.com/user-attachments/assets/d6f8b13c-d3fe-4f76-9f83-38e02f5c87f4)
   **The above graph shows the Temporal Trends of Protests.**
   
   ![image](https://github.com/user-attachments/assets/f688ac1d-0c2b-4fb8-944e-ce49c03b22f2)
   **The above graph shows some of the protests' characteristics.**
   
   ![image](https://github.com/user-attachments/assets/1fa3806e-d37b-43c5-9d2d-4c1614113232)
   **The above graph shows the State Responses to Protests**
   
4. #### Modeling
   - **Purpose:** Modeling and analysis of state responses using various machine learning algorithms.
   - **Key Actions:**
   - - Implemented Logistic Regression, Random Forest, Gradient Boosting and XGBoost models.
     - Evaluated model performance using accuracy, precision, recall, F1-scores, and ROC-AUC.
     - The final XGBoost model was deployed using Streamlit.
       ![image](https://github.com/user-attachments/assets/9740bb03-8d0d-4229-8233-005d07c6fbe8)
       **The above image shows the ROC-AUD Curves for XGBoost model.**
       
       ![image](https://github.com/user-attachments/assets/55218160-af9c-48e7-b561-58da3762c46c)
       **The above image shows the confusion matrix for XGBoost model**
       
 5. #### Sentimental analysis on Notes in mass protests.
    - **Purpose:** Sentiment analysis of protest notes.
    - **Key Actions:**
      - Preprocessed text data.
      - Calculated sentiment scores (positive, negative, neutral).
      - Visualized sentiment distribution and common themes.
        ![image](https://github.com/user-attachments/assets/7419400a-6f37-4877-ba8f-f47e452f53c9)
        **The above graph shows the Sentiment Distribution**
        
        ![image](https://github.com/user-attachments/assets/49e5dd07-11b9-4cfc-87ee-8f7cafac1654)
        **The above is one of the word clouds for Topic 1 sentiments.**
        
        ![image](https://github.com/user-attachments/assets/e167208e-4149-411d-a9a1-4c722cfac714)
        **The above bar chart shows the Trigam analysis**
        
  6. #### Tweets Sentimental Analysis:
     - **Purpose:** Sentiment analysis on tweets from 13th July 2024 to 23rd July 2024.
     - **Key Actions:**
     - - Preprocessed tweet data.
       - Analyzed sentiment trends in the tweets.
         ![image](https://github.com/user-attachments/assets/8838e987-35fc-426e-ba4a-12f7ce6cd3c3)
         **The above bar chart shows the sentiment distribution in tweets.**
         
         ![image](https://github.com/user-attachments/assets/077412d2-758b-4b6c-ba58-d2042e4b9d25)
         **Word cloud for tweet sentiments**
         
## Deployment
The final model for predicting state responses was deployed using Streamlit.
You can access the applications here:
- Protest Outcome Prediction Model https://protests.streamlit.app/
- Mass Mobilization Analytics https://mass-protests.streamlit.app/

## Conclusion
The analysis of global protest events from 1990 to 2020, combined with sentiment analysis of tweets from 13th July 2024 to 23rd July 2024 highlights the complexity and importance of understanding socio-political unrest. The insights gained emphasize how the state will respond to the protests.
## Acknowledgments
Special thanks to our Technical mentors Noah Kandie and Bonface Manyara for their immense contribution to this project. The dataset used was from the Havard mass mobilization dataset. https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/HTTWYL/TJJZNG and scraped tweets from X.
## Authors
**Magdalene Ondimu**

**Najma Abdi**

**Brian Kariithi**

**Leon Maina**

**Wilfred Lekish**

       



