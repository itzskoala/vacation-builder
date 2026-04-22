import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from serpapi import Client


def _get_client() -> Client:
    return Client(api_key=os.getenv("SERPAPI_API_KEY"))

#this is the format we want the flight data to be returned in
class FlightSearchInput(BaseModel):
    departure_id: str = Field(
        ...,
        description="IATA airport or city code for departure (e.g. 'LAX', 'JFK', 'NYC')"
    )
    arrival_id: str = Field(
        ...,
        description="IATA airport or city code for arrival (e.g. 'CDG', 'NRT', 'TYO')"
    )
    outbound_date: str = Field(
        ...,
        description="Outbound flight date in YYYY-MM-DD format"
    )
    return_date: str = Field(
        ...,
        description="Return flight date in YYYY-MM-DD format"
    )
    currency: str = Field(
        default="USD",
        description="Currency code for prices (e.g. 'USD', 'EUR', 'CLP', 'INR', 'MXN')"
    )
    gl: str = Field(
        default="us",
        description=(
            "Google country code to simulate searching from a specific region. "
            "Different regions surface different airline deals, local fares, and pricing. "
            "Examples: 'us' (United States), 'cl' (Chile), 'mx' (Mexico), 'br' (Brazil), "
            "'ar' (Argentina), 'gb' (United Kingdom), 'de' (Germany), 'jp' (Japan), 'in' (India). "
            "Use this to find regional pricing differences — the same flight is often cheaper "
            "when searched from the destination country or the airline's home market."
        )
    )


class GoogleFlightsTool(BaseTool):
    name: str = "Google Flights Search"
    description: str = (
        "Search for round-trip flights using Google Flights. "
        "Provide IATA airport or city codes, travel dates, preferred currency, and a country "
        "code (gl) to simulate searching from a specific region. "
        "The same flight can cost significantly less when searched from a different country — "
        "for example, a route served by a Latin American carrier may be cheaper when searched "
        "from that carrier's home market. Call this tool multiple times with different gl/currency "
        "combinations to compare regional prices and find the best deal. "
        "Returns top flight options with airline, duration, stops, and price."
    )
    args_schema: Type[BaseModel] = FlightSearchInput

    def _run(
        self,
        departure_id: str,
        arrival_id: str,
        outbound_date: str,
        return_date: str,
        currency: str = "USD",
        gl: str = "us",
    ) -> str:
        try:
            client = _get_client()
            results = client.search({
                "engine": "google_flights",
                "departure_id": departure_id,
                "arrival_id": arrival_id,
                "outbound_date": outbound_date,
                "return_date": return_date,
                "currency": currency,
                "hl": "en",
                "gl": gl,
                "type": "1",  # round trip
            })

            flights = results.get("best_flights", []) or results.get("other_flights", [])
            if not flights:
                return "No flights found for the given parameters."

            output = []
            for i, flight in enumerate(flights[:5], 1):
                legs = flight.get("flights", [])
                price = flight.get("price", "N/A")
                total_duration = flight.get("total_duration", "N/A")

                leg_summaries = []
                for leg in legs:
                    dep = leg.get("departure_airport", {})
                    arr = leg.get("arrival_airport", {})
                    leg_summaries.append(
                        f"  {leg.get('airline', '')} {leg.get('flight_number', '')} | "
                        f"{dep.get('id', '')} → {arr.get('id', '')} | "
                        f"Departs: {dep.get('time', '')} | "
                        f"Arrives: {arr.get('time', '')}"
                    )

                output.append(
                    f"Option {i}: {price} {currency} | Region: {gl.upper()} | Total Duration: {total_duration} min\n"
                    + "\n".join(leg_summaries)
                )

            return "\n\n".join(output)
        except Exception as e:
            return f"Flight search failed: {str(e)}"

#this is the format we want the Hotel search to take
class HotelSearchInput(BaseModel):
    query: str = Field(
        ...,
        description="Hotel search query (e.g. 'hotels in Paris near city center')"
    )
    check_in_date: str = Field(
        ...,
        description="Check-in date in YYYY-MM-DD format"
    )
    check_out_date: str = Field(
        ...,
        description="Check-out date in YYYY-MM-DD format"
    )
    currency: str = Field(
        default="USD",
        description="Currency code for prices (e.g. 'USD', 'EUR')"
    )


class GoogleHotelsTool(BaseTool):
    name: str = "Google Hotels Search"
    description: str = (
        "Search for hotels, Airbnbs, and other accommodations using Google Hotels. "
        "Aggregates pricing from Booking.com, Expedia, Hotels.com, and more in one call. "
        "Provide a location query, check-in/check-out dates, and currency. "
        "Returns top options with name, rating, price per night, amenities, and booking link."
    )
    args_schema: Type[BaseModel] = HotelSearchInput

    def _run(
        self,
        query: str,
        check_in_date: str,
        check_out_date: str,
        currency: str = "USD",
    ) -> str:
        try:
            client = _get_client()
            results = client.search({
                "engine": "google_hotels",
                "q": query,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "currency": currency,
                "hl": "en",
            })

            properties = results.get("properties", [])
            if not properties:
                return "No accommodations found for the given parameters."

            output = []
            for i, hotel in enumerate(properties[:8], 1):
                name = hotel.get("name", "Unknown")
                rating = hotel.get("overall_rating", "N/A")
                reviews = hotel.get("reviews", "N/A")
                price = hotel.get("rate_per_night", {}).get("lowest", "N/A")
                hotel_class = hotel.get("hotel_class", "")
                amenities = ", ".join(hotel.get("amenities", [])[:5])
                link = hotel.get("link", "")

                output.append(
                    f"{i}. {name} {hotel_class}\n"
                    f"   Rating: {rating}/5 ({reviews} reviews) | Price/night: {price}\n"
                    f"   Amenities: {amenities}\n"
                    f"   Link: {link}"
                )

            return "\n\n".join(output)
        except Exception as e:
            return f"Hotel search failed: {str(e)}"


#this is the format we want the Images search to take
class ImageSearchInput(BaseModel):
    query: str = Field(
        ...,
        description="Image search query (e.g. 'Kyoto Japan cherry blossom temples landscape')"
    )
    num_results: int = Field(
        default=10,
        description="Number of image results to return (max 20)"
    )


class GoogleImagesTool(BaseTool):
    name: str = "Google Images Search"
    description: str = (
        "Search for high-quality travel photos using Google Images. "
        "Returns actual inline markdown images ready to embed in documents. "
        "Use these image embeds directly in your output — do NOT rewrite them as links or queries."
    )
    args_schema: Type[BaseModel] = ImageSearchInput

    def _run(self, query: str, num_results: int = 10) -> str:
        try:
            client = _get_client()
            results = client.search({
                "engine": "google_images",
                "q": query,
                "hl": "en",
                "num": min(num_results, 20),
            })

            images = results.get("images_results", [])
            if not images:
                return "No images found for the given query."

            output = []
            for i, img in enumerate(images[:num_results], 1):
                title = img.get("title", "Untitled")
                # prefer thumbnail (Google-proxied, reliably embeddable); fall back to original
                url = img.get("thumbnail", "") or img.get("original", "")
                source = img.get("source", "")

                if url:
                    # Return ready-to-use markdown image embed
                    output.append(
                        f"**{i}. {title}**\n"
                        f"![{title}]({url})\n"
                        f"*Source: {source}*"
                    )

            if not output:
                return "No usable image URLs found for the given query."

            return "\n\n".join(output)
        except Exception as e:
            return f"Image search failed: {str(e)}"

#this is the format we want the Images search to take
class EventSearchInput(BaseModel):
    query: str = Field(
        ...,
        description="Event search query including destination and dates (e.g. 'events in Tokyo May 2026')"
    )


class GoogleEventsTool(BaseTool):
    name: str = "Google Events Search"
    description: str = (
        "Search for local events, festivals, concerts, and activities using Google Events. "
        "Provide a query including the destination and travel dates. "
        "Returns upcoming events with name, date, venue, and description."
    )
    args_schema: Type[BaseModel] = EventSearchInput

    def _run(self, query: str) -> str:
        try:
            client = _get_client()
            results = client.search({
                "engine": "google_events",
                "q": query,
                "hl": "en",
            })

            events = results.get("events_results", [])
            if not events:
                return "No events found for the given query."

            output = []
            for i, event in enumerate(events[:10], 1):
                name = event.get("title", "Unknown Event")
                date_info = event.get("date", {})
                date_str = f"{date_info.get('start_date', '')} {date_info.get('when', '')}".strip()
                venue = event.get("address", [])
                venue_str = ", ".join(venue) if isinstance(venue, list) else str(venue)
                description = (event.get("description") or "")[:200]
                link = event.get("link", "")

                output.append(
                    f"{i}. {name}\n"
                    f"   Date: {date_str}\n"
                    f"   Location: {venue_str}\n"
                    f"   {description}\n"
                    f"   Link: {link}"
                )

            return "\n\n".join(output)
        except Exception as e:
            return f"Events search failed: {str(e)}"
