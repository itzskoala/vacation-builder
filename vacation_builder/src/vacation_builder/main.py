#!/usr/bin/env python
import sys
import os
import warnings

from vacation_builder.crew import VacationBuilder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")



def run():
    """
    Run the VacationBuilder crew.
    Update the inputs below to test with different destinations and preferences.
    """
    
    print("Hey welcome! Let's build your Dream Vacation!\n")
    print("If you have no prefrences, just type 'N/A' for any input and we'll work our magic ;)\n")
    location = input("Where do you want to go? (e.g, country, city, town)\n")
    origin = input("Where are you currently located?\n")
    method_of_travel = input("How will you get there? (e.g, car, plane, cruise?)\n")
    group_size = input("Who's going on this trip? (e.g. solo, couple, family with kids, group of friends)\n")
    budget = input("What is your budget range? You can type in a number, range, or a description (e.g. Dirt Cheap, Low, Mid, High, or Splurge)\n")
    time_frame = input("What is your time frame? (e.g. May 1 - May 10, 2026).\n")
    activity_preferences = input("What kind of activities are you into? (e.g. beach, hiking, nightlife, museums, food tours)\n")
    extra_prefrences = input("Is there anything else we should know about this trip?\n")


    inputs = {
        "location": location,
        "origin": origin,
        "method_of_travel": method_of_travel,
        "group_size": group_size,
        "budget": budget,
        "time_frame": time_frame,
        "activity_preferences": activity_preferences,
        "extra_prefrences": extra_prefrences,
    }

    os.makedirs("output", exist_ok=True)

    try:
       result = VacationBuilder().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occured while running the crew {e}")

    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

if __name__ == "__main__":
    run()