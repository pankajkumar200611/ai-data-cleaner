import pandas as pd
import re
import numpy as np
import google.generativeai as genai

def process_query(query, df, api_key=None):
    """
    Advanced AI Assistant. Uses Gemini if API key is provided, otherwise falls back to local rules.
    """
    query = query.lower()
    
    # --- GEMINI AI INTEGRATION ---
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Prepare dataset context
            context = f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns.\n"
            context += f"Columns and Types:\n{df.dtypes.to_string()}\n\n"
            context += f"Summary Statistics:\n{df.describe().to_string()}\n\n"
            context += f"First 5 rows preview:\n{df.head().to_string()}\n\n"
            
            prompt = f"You are an expert Data Analyst AI for 'DataCleaner AI'. You are analyzing the user's dataset. Answer the following question based ONLY on the dataset context provided below.\n\nContext:\n{context}\nUser Question: {query}"
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"⚠️ **Gemini API Error:** {str(e)}\n\n*Falling back to local AI mode...*"

    # --- LOCAL RULE-BASED AI (FALLBACK) ---
    # 1. Missing Values
    if re.search(r'null|missing|nan|empty|blank', query):
        null_counts = df.isnull().sum()
        cols_with_nulls = null_counts[null_counts > 0]
        if cols_with_nulls.empty:
            return "Good news! There are no missing values in this dataset."
        else:
            res = "Here are the columns with missing values:\n"
            for col, count in cols_with_nulls.items():
                pct = (count / len(df)) * 100
                res += f"- **{col}**: {count} missing ({pct:.1f}%)\n"
            return res
            
    # 2. Duplicates
    elif re.search(r'duplicate|repeat|copy', query):
        duplicates = df.duplicated().sum()
        if duplicates == 0:
            return "There are no duplicate rows in the dataset. It's clean!"
        else:
            pct = (duplicates / len(df)) * 100
            return f"I found **{duplicates}** duplicate rows in your dataset (that's {pct:.1f}% of the data)."
            
    # 3. Shape / Size
    elif re.search(r'shape|size|how many rows|how many columns|dimension', query):
        rows, cols = df.shape
        return f"The dataset has **{rows}** rows and **{cols}** columns. Total cells: {rows * cols}."
        
    # 4. Data Types
    elif re.search(r'type|data type|format|kind of data', query):
        res = "Here is the breakdown of your column data types:\n"
        for col, dtype in df.dtypes.items():
            res += f"- **{col}**: `{dtype}`\n"
        return res
        
    # 5. Outliers
    elif re.search(r'outlier|extreme|anomaly', query):
        num_cols = df.select_dtypes(include=['number']).columns
        if len(num_cols) == 0:
            return "There are no numerical columns to check for outliers."
        
        res = "Checking numerical columns for outliers (values > 3 standard deviations from the mean):\n"
        found_outliers = False
        for col in num_cols:
            mean = df[col].mean()
            std = df[col].std()
            outliers = df[(df[col] < mean - 3 * std) | (df[col] > mean + 3 * std)]
            if len(outliers) > 0:
                found_outliers = True
                res += f"- **{col}**: Found {len(outliers)} potential outliers.\n"
        
        if not found_outliers:
            return "I couldn't find any obvious extreme outliers (using the 3 std-dev rule)."
        return res + "\nYou can use the 'Remove Outliers' option in the cleaning panel to filter these out."

    # 6. Unique values
    elif re.search(r'unique|distinct|different values', query):
        res = "Here is the count of unique values in each column:\n"
        for col in df.columns:
            uniques = df[col].nunique()
            res += f"- **{col}**: {uniques} unique values\n"
        return res

    # 7. Summary Statistics / Averages
    elif re.search(r'average|mean|median|min|max|summary|statistics|describe', query):
        num_cols = df.select_dtypes(include=['number']).columns
        if len(num_cols) == 0:
            return "There are no numerical columns to calculate statistics for."
        
        desc = df[num_cols].describe().round(2)
        res = "Here is a quick statistical summary of your numerical columns:\n\n"
        for col in num_cols:
            res += f"**{col}**:\n"
            res += f"- Average (Mean): {desc.loc['mean', col]}\n"
            res += f"- Min: {desc.loc['min', col]} | Max: {desc.loc['max', col]}\n\n"
        return res
        
    # 8. Memory Usage
    elif re.search(r'memory|size in memory|ram|bytes', query):
        mem_bytes = df.memory_usage(deep=True).sum()
        mem_mb = mem_bytes / (1024 * 1024)
        return f"This dataset is currently using approximately **{mem_mb:.2f} MB** of memory."

    # 9. Smart Suggestions
    elif re.search(r'suggest|what should i do|help|recommend', query):
        suggestions = ["Based on my automated analysis, I suggest you:"]
        
        if df.isnull().sum().sum() > 0:
            suggestions.append("1. **Handle Missing Values**: I spotted empty cells. Use the AI Cleaning Panel to drop them or fill them with the mean/mode.")
        
        if df.duplicated().sum() > 0:
            suggestions.append("2. **Remove Duplicates**: I detected duplicate rows. You should clean them up to prevent model bias.")
            
        object_cols = df.select_dtypes(include=['object']).columns
        if len(object_cols) > 0:
            suggestions.append(f"3. **Encode Categorical Data**: You have {len(object_cols)} text columns. Consider encoding them if you plan to build machine learning models.")
            
        if len(suggestions) == 1:
            return "Your dataset looks pretty clean! You might want to normalize numerical data or double-check for extreme outliers."
            
        return "\n".join(suggestions)
        
    # Default Fallback
    else:
        return ("I'm your local AI Data Assistant! I don't use external servers, so I can safely analyze your data here. Try asking me:\n"
                "- 'Which columns contain **missing** values?'\n"
                "- 'Are there any **duplicate** rows?'\n"
                "- 'Show me **unique** value counts.'\n"
                "- 'Calculate the **average, min, and max**.'\n"
                "- 'Check for **outliers**.'\n"
                "- 'What is the **memory** usage?'\n"
                "- '**Suggest** preprocessing steps.'")
