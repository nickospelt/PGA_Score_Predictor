def clean_tournament_results(position, earnings, player_name, name_mappings):
    new_position = position
    if (new_position[0] == 'T'):
        new_position = new_position[1:]
    elif (new_position[0] == '-'):
        new_position = None

    new_earnings = ""
    if (earnings != "--"):
        earnings_parts = earnings.split(",")
        if (len(earnings_parts) == 2):
            new_earnings = earnings_parts[0][1:] + earnings_parts[1]
        else:
            new_earnings = earnings_parts[0][1:] + earnings_parts[1] + earnings_parts[2]
    else:
        new_earnings = None

    new_player_name = player_name
    if (new_player_name in name_mappings):
        new_player_name = name_mappings[new_player_name]

    return new_position, new_earnings, new_player_name

name_mappings = {
        "Sami Välimäki": "Sami Valimaki", 
        "Séamus Power": "Seamus Power",
        "Matt Fitzpatrick": "Matthew Fitzpatrick",
        "Gunnar Broin (a)": "Gunnar Broin",
        "Luke Clanton (a)": "Luke Clanton",
        "Joaquín Niemann": "Joaquin Niemann",
        "Sebastian Söderberg": "Sebastian Soderberg",
        "Blaine Hale, Jr.": "Blaine Hale Jr.",
        "Gordon Sargent (a)": "Gordon Sargent",
        "Nicolai Højgaard": "Nicolai Hojgaard",
        "Pablo Larrazábal": "Pablo Larrazabal",
        "Rasmus Højgaard": "Rasmus Hojgaard",
        "Matt NeSmith": "Matthew NeSmith",
        "Stewart Hagestad (a)": "Stewart Hagestad",
        "Travis Vick (a)": "Travis Vick",
        "Mike Lorenzo-Vera": "Michael Lorenzo-Vera",
        "Richard H. Lee": "Richard Lee",
        "Taehee Lee": "Tae Hee Lee",
        "Matt Parziale (a)": "Matt Parziale",
        "Seung-su Han": "Seungsu Han",
        "Dan Obremski": "Daniel Obremski",
        "Grady Brame Jr.": "Grady Brame",
        "Jordan Smith": "Jordan L Smith"
    }

print(clean_tournament_results("-", "--", "Sami Välimäki", name_mappings))