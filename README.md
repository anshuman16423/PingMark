# PingMark
Discord BOT built on python to handle competitive programming utilities on the Institute discord server.

- The BOT aims to simplify viewing user activities, contest ranklists, rating changes etc. on competitve programming platforms [codechef and codeforces]
- The BOT bundles all the handles of the users in the server in a single ranklist to simplyfy the search of common ranklist for the server.
- The BOT also facillitates easy sharing of previous submissions made on the CP platforms on the server itself, and hence making the CP Discussions on the server smoother than ever! .
- The BOT makes the use of the codeforces API.
- The python script uses python's pickle module to store handles of the server users in the database.


## Why this BOT ?
Competitive programmers regularly check for the ranklists/user ratings changes/upcoming contests etc , this BOT solves the problem by quickly giving results on one line commands instead of browsing through multiple pages.
Moreover the BOT can be easily accesed by smartphones as well as PC's.
BOT also helps in quality discussions on the CP forum by posting the required source code in the conversation  itself, hence making the forum efficient.

## Requirements

- Python 3.7
- Installing Additional Python Libraries
	-	> pip3 install bs4
	-	> pip3 install discord
- Create a file token.txt in the same directory and copy paste your discord BOT token in the text file.

### Getting started with BOT commands
 - add_CC::username -> maps a valid codechef username to the server user.
 - add_CF::username -> maps a valid codeforces username to the server user.
 - CC_rating::username -> extracts the current codechef user rating.
 - CF_rating::username -> extracts current codeforces user rating. when given username "all" prints a list of all user ratings in the server.
 - CF_code::contest_code::solution_code -> prints the source code for the submission made on codeforces.
 - CF_contest::contest_code -> returns ranklist for a codeforces round filtered for the server memebers.
 - CC_code::submission_number -> prints the source code of a submission made on codechef.

### upcoming features / commands
 
 - [ ] CC_contest -> CF_contest for codechef.
 - [ ] CF_question -> display codeforces question to facillitate question discussions in the server.
 - [ ] add_CF -> further enhance the authenticity of handles mapped with a server client.
 - [ ] CF_alarm -> set codeforces event reminders.




