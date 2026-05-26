from pathlib import Path
import sys
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
import os
    
# am i stupid

def current_exe_dir():
    if getattr(sys, 'frozen', False):
        # Running as bundled executable
        current_path = Path(sys.executable).parent
    else:
    # Running as normal Python script
        current_path = Path(__file__).resolve().parent

def collectData_Type():
    print("Welcome to Licensr Wizard. This wizaed will help you recommend one.")
    print("\n Lets begin with our Wizard now!")
    res_typeof_project = inquirer.select(
        message="What is the type of your project?",
        choices=[
            Choice("Library/Framework"),
            Choice("Application"),
            Choice("Documentation"),
            Choice("Other")
        ],
    ).execute()
    return res_typeof_project

def collectData_effort():
    res_effort = inquirer.select(
        message="How much effort did you poured into making this project?",
        choices=[
            Choice("A lot of effort"),
            Choice("Some effort"),
            Choice("Not much effort"),
            Choice("I just threw it together")
        ]
    ).execute()
    return res_effort

def collectData_usageByOthers(): 
    res_usage_by_others = inquirer.select(
        message="Who do you think this project will be used by?",
        choices=[
            Choice("Everyone, Including Companies (Commercial Purposes)"),
            Choice("Everyone, But Not Companies (Non-Commercial Purposes)"),
        ]
    ).execute()
    return res_usage_by_others

def collectData_Attribution():
    res_attribution = inquirer.select(
        message="Do you want to be attributed for your work?",
        choices=[
            Choice("Yes, I want to be attributed"),
            Choice("Attribution preferred, but not required"),
            Choice("No, I don't care about attribution")
        ]
    ).execute()
    return res_attribution

def collectData_Copyleftation():
    res_copyleftation = inquirer.confirm(
        message="Do you care about sharing improvements?"
    ).execute()
    return res_copyleftation

def collectData_PatentProtection():
    res_patent_protection = inquirer.confirm(
        message="Do you want to provide patent protection for users of your project?"
    ).execute()
    return res_patent_protection

def collectData_sublicensing():
    res_sublicensing = inquirer.confirm(
        message="Do you want to allow people to release modified versions of your project under a different license?"
    ).execute()
    return res_sublicensing

def scoring():
    p_type = collectData_Type()
    score = 0
    if (p_type == "Library/Framework"):
        score = 1
    elif (p_type == "Application"):
        score = 2
    else:
        score = 0

    effort = collectData_effort()
    if (effort == "A lot of effort"):
        score += 2
    elif (effort == "Some effort"):
        score += 1
    else:
        score += 0
    
    usage_by_others = collectData_usageByOthers()
    strict_score = 0
    if (usage_by_others == "Everyone, Including Companies (Commercial Purposes)"):
        strict_score = 0
    elif (usage_by_others == "Everyone, But Not Companies (Non-Commercial Purposes)"):
        strict_score = 1

    if strict_score == 1: 
        score = 199 # Custom Score to allow CC-NC License.

    attribution = collectData_Attribution()
    if (attribution == "Yes, I want to be attributed"):
        score += 2
    elif (attribution == "Attribution preferred, but not required"):
        score += 1

    copyleftation = collectData_Copyleftation()
    if (copyleftation):
        score += 2
    else:
        score += 0

    patent_protection = collectData_PatentProtection()
    if (patent_protection):
        score += 1
    else: 
        score += 0

    sublicensing = collectData_sublicensing()
    if (sublicensing):
        score += 0
    else:
        score += 3

    return score

def license_recommendation(score):
    # Special non-open-source case

    # Ultra permissive
    if 0 <= score <= 1:
        return "MIT No Attribution License (MIT-0)"

    # Permissive
    elif 2 <= score <= 3:
        return "MIT License"

    # Permissive + patent protection
    elif 4 <= score <= 5:
        return "Apache License 2.0"

    # Weak copyleft
    elif 6 <= score <= 7:
        return "Mozilla Public License 2.0 (MPL-2.0)"

    # Library-focused copyleft
    elif 8 <= score <= 9:
        return "GNU Lesser General Public License v3.0 (LGPL-3.0)"

    # Strong copyleft
    elif 10 <= score <= 11:
        return "GNU General Public License v3.0 (GPL-3.0)"

    # Very strong/network copyleft
    elif score >= 12 and score <= 100:
        return "GNU Affero General Public License v3.0 (AGPL-3.0)"
    
    elif score >= 100: 
        return "Creative Commons Attribution-NonCommercial License (CC BY-NC 4.0)"

    # Fallback
    return "Unable to determine suitable license"
    
def collectData():
    score = scoring()
    license = license_recommendation(score)
    console = Console()
    console.print(f"\nBased on your answers, we recommend you to use the [bold green]{license}[/bold green] license for your project!", style="bold blue")
    console.print("\nThank you for using Licensr Wizard! If you have any feedback or suggestions, please let us know.", style="bold magenta")
    console.print("Note that Licensr doesn't give legal Advice, so please consult with a legal professional before making any final decisions about your project's license.", style="bold red")


if __name__ == "__main__":
    collectData()