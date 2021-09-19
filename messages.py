def get_pretty_message(course, year, lessons):
    header = f'🎓 *{course}, {year}*\n\n'
    final_message = ""
    for single_lesson in lessons:
        place = single_lesson["description"].split(" <div style=\"height:8px\"></div><b>Docenti:</b> ")[0]
        teacher = single_lesson["description"].split(" <div style=\"height:8px\"></div><b>Docenti:</b> ")[1]
        final_message = final_message + f'⚪️ *{single_lesson["title"]} - {single_lesson["anno"]}° anno*\n*{teacher}*\n{place}\n_{single_lesson["tester"]}_\n\n\n'
    if final_message == "":
        final_message= "Non sono presenti materia nella data e facoltà selezionate."
    return header+final_message

def get_startup_message():
    return f'Benvenuto!\nScrivi /orari per iniziare!'