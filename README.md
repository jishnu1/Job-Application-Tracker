# Instructions

* Install dependencies
* Make a copy of the template folder and rename it
* Update the file path for the new variables.json in the last line of job_application_tracker.py <br>
  * use the example folder to see how the program works
  * use your new folder to create your own job application tracker
  * do not use the original template folder since the data is invalid
* Edit the values in variables.json
  * INPUT_FILE - update folder name
  * OUTPUT_FILE - update folder name
  * ERROR_FILE - update folder name
  * DATA_FILE - update folder name
  * RETRIES - number of times to retry failed http requests <br>
  (3 should be enough but you can increase to 5 to be extra safe)
  * SKIP_OLD_COMPANIES - setting to 1 will skip over companies that already have data in the input file
* Add Glassdoor company URLs to the Glassdoor column in tracker_old.csv <br>
  * Use the full length URL
  * Correct: https://www.glassdoor.com/Overview/Working-at-Meta-EI_IE40772.11,15.htm
  * Incorrect: https://www.glassdoor.com/metacareers
  * If Glassdoor does not use the full URL by default, manually search for the company, inspect the page, and copy the path in the "href" value
  * Example: href="/Overview/Working-at-Meta-EI_IE40772.11,15.htm"
* Run job_application_tracker.py <br>

# Tips

* Upload your job application tracker to Google Sheets for more functionality