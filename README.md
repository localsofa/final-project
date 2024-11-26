# LANGUAGE DATA COLLECTOR

#### Description:
This project is an attempt to create a linguistic database with several language inputs, created by users by accessing a website.
This database features a sentence from the user, the language the sentences is in (inputted by the user themselves), the regional dialect the user is using, and
finally the chosen name of the user.

The database then displays all inputs in a large table which the user can access, and then allows for filtering via two drop-down menus.
The user must first filter by language, and then has the option to select a certain dialect. If they have added a language or dialect
which has not been used yet, these will appear in the menu as well.

Once the user has selected the language or dialect, the table will update to only show that distinct selection.

- IMPORTANT: The user must FIRST filter by language.



#### PYTHON:
The python file is broken down into two functions: after_request() and index().

The first thing app.py does is generate a randomized secret key which allows flask to use flash. This is necessary for the
error message to display.

##### after_request(response)
This function then prevents the browser from caching any user responses.
- `no-cache`: response should not be cached
- `no-store`: prevents storing of cached copy
- `must-revalidate`: cache must check with server before using cached response
- `Expires: 0`: sets "expiration date" of response to past
- `Pragma: no-cache`: further prevents caching
- `return response`: returns object response to client


##### index()
Then, it assigns the inputted values from the form in index.html to seperate values, distinguishing languages
and dialect for later filtering.

1. Routes and Methods
    - GET: display existing entries from database
    - POST: submit data entered in form

2. Form Submission
    - When the user submits the form, the following data is retrieved: <br>
        - `name`: Name of user <br>
        - `sentences`: Sentence(s) submitted by user <br>
        - `selected_language`: Language selected by user <br>
        - `selected_dialect`: Dialect selected by user <br>

    - If there are empty fields, a message is flashed to fill out all fields:


        ```python
        if not name or not sentences or not selected_language or not selected_dialect:
            flash("Please fill out all fields.")
            return redirect("/")
        ```

    - If all fields are filled out, the data is added to the database:


        ```python
        db.execute("INSERT INTO sentences (name, sentences, language, dialect) VALUES (:name, :sentences, :language, :dialect)",
           name = name, sentences = sentences, language = selected_language, dialect = selected_dialect)
        ```


    - User is then redirected to the updated page:

        ```python
        return redirect("/")
        ```


3. Display existing entries
    - function retrieves data from database
        - all rows from `sentences` table
        - distinct languages from `sentences` table to show as filter options

        ```python
        rows = db.execute("SELECT * FROM sentences")
        distinct_languages = db.execute("SELECT DISTINCT language FROM sentences")
        ```
4. Filtering
    - If a language has been selected, the funciton retrieves the dialect selection for that language and filters the rows based on the selected language.
    ```python
    if selected_language:
    distinct_dialects = db.execute("SELECT DISTINCT dialect FROM sentences WHERE language = :language", language = selected_language)
    filtered_rows = [row for row in rows if row["language"] == selected_language]

    if selected_dialect:
        filtered_rows = [row for row in filtered_rows if row["dialect"] == selected_dialect]
    ```

    - If no language is selected, all rows are displayed without filtering.
    ```python
    else:
    distinct_dialects = []
    filtered_rows = rows
    ```

5. Rendering template
    - index.html is then rendered with rows filtered by language and dialect.
    ```python
    return render_template("index.html", rows = filtered_rows, distinct_languages = distinct_languages, distinct_dialects = distinct_dialects, selected_dialect = selected_dialect)
    ```

6. Further considerations
    - I considered adding langdetect() to automatically determine the language, but I felt that the usage of dialects would
    get in the way of this process, and the primary objective is to collect specific regional data as well, so I allowed the user
    to submit the language manually as well.

#### SQL:

The database contains a table `sentences`, with four columns:
- `name`
- `sentences`
- `langauge`
- `dialect`

#### HTML:

1. Form
- The HTML file "index.html" has a form with four different possible inputs:
    - `name`
    - `sentence`
    - `language`
    - `dialect`

The user must fill out all of these fields, otherwise an error message is delivered using flash.

- Underneath the form, there is the first of two filters. This one creates a dropdown menu of all values inputted to "language",
and if the value is submitted for the first time, the for loop adds the value to the menu. When the user selects a languages and then
clicks the "Filter" button, only inputs from that language are shown.

    ```HTML
        {% for language in distinct_languages %}
            <option value = "{{ language['language'] }}" {% if request.args.get("language") == language["language"] %}selected{% endif %}>
            {{ language["language"] }}
            </option>
        {% endfor %}
    ```

After, the user is able to further filter the results by selecting a dialect from the dropdown menu which functions the same as the
"languages" one. However, only the general language is shown in the table, not the dialect. When the user clicks the button assigned
"submit", the page reloads and displays only the selected language and/or dialect.

#### CSS:
The style sheet modifies:
- `body`
- `h1` heading
- `button` (all of the same class)
- `input`
- `table`, `th`, `td`
- every odd row of `tbody`

##### class
- .container
- .header
- .section
- .section:hover
