import os
import pandas as pd
import streamlit as st
from pymongo import MongoClient
from analyze_v4 import load_full_grid, MIRROR_CACHE, PARTNER_ISO_TO_NAME
from what_if_simulator import build_analog_library_profiles

GROUP_COLS = ["reporterISO", "reporterDesc", "cmdCode", "commodity_name", "flowDesc"]
MONTHLY_CACHE = "monthly_series_cache.csv"

@st.cache_resource
def get_mongo_client():
    # Connects to your local MongoDB instance
    return MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)

@st.cache_data(ttl=600)
def load_combined_grid():
    # 1. Try to load from MongoDB (The NoSQL Serving Layer)
    try:
        client = get_mongo_client()
        db = client["trade_disruption_db"]
        collection = db["monthly_trade_series"]
        
        # Fetch data from MongoDB
        docs = list(collection.find({}, {"_id": 0}))
        
        if docs:
            records = []
            for doc in docs:
                # Flatten the nested JSON structure back into a table
                records.append({
                    "reporterISO": doc["metadata"]["reporterISO"],
                    "reporterDesc": doc["metadata"]["reporterDesc"],
                    "cmdCode": doc["metadata"]["cmdCode"],
                    "commodity_name": doc["metadata"]["commodity_name"],
                    "flowDesc": doc["metadata"]["flowDesc"],
                    "period": int(doc["timestamp"].strftime("%Y%m")),
                    "trade_value": doc["trade_value"],
                })
            reporter_full = pd.DataFrame(records)
            reporter_full["is_observed"] = reporter_full["trade_value"].notna()
            
            st.session_state["db_status"] = "MongoDB (NoSQL)"
        else:
            raise ValueError("MongoDB collection is empty.")

    except Exception as e:
        # 2. Fallback to CSV if MongoDB is not running
        st.session_state["db_status"] = "CSV Fallback"
        if not os.path.exists(MONTHLY_CACHE):
            return None
        reporter_full = load_full_grid(MONTHLY_CACHE, GROUP_COLS)

    # 3. Add Mirror Data (still from CSV for simplicity)
    combined = reporter_full[~reporter_full["reporterDesc"].isin(PARTNER_ISO_TO_NAME.values())].copy()

    if os.path.exists(MIRROR_CACHE):
        mirror_raw = pd.read_csv(MIRROR_CACHE)
        mirror_raw["period"] = mirror_raw["refYear"] * 100 + mirror_raw["refMonth"]
        mirror_raw = mirror_raw[mirror_raw["partnerISO"].isin(PARTNER_ISO_TO_NAME.keys())].copy()
        mirror_raw["reporterISO"] = mirror_raw["partnerISO"]
        mirror_raw["reporterDesc"] = mirror_raw["partnerISO"].map(PARTNER_ISO_TO_NAME)

        all_periods = [y * 100 + m for y in range(2017, 2026) for m in range(1, 13) if y * 100 + m <= 202512]
        mkeys = mirror_raw[GROUP_COLS].drop_duplicates()
        mfull_idx = mkeys.merge(pd.DataFrame({"period": all_periods}), how="cross")
        mfull = mfull_idx.merge(mirror_raw[GROUP_COLS + ["period", "trade_value"]], on=GROUP_COLS + ["period"], how="left")
        mfull["is_observed"] = mfull["trade_value"].notna()
        combined = pd.concat([combined, mfull], ignore_index=True)

    return combined

@st.cache_data
def get_analog_library():
    return build_analog_library_profiles()