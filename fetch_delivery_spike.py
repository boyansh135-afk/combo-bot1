import requests

def fetch_delivery_spike():
    try:
        # Dummy delivery spike logic — replace with actual logic or API if needed
        # Example: Get stocks with unusual delivery %
        # You can integrate NSE India or use static logic for now
        delivery_spikes = ["RELIANCE", "TATASTEEL", "HINDALCO"]
        msgs = [f"🚚 Delivery spike in {stock}" for stock in delivery_spikes]
        return msgs

    except Exception as e:
        return [f"⚠️ Error in delivery spike: {e}"]