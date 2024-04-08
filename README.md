# game_of_thrones

Wonder Team of 3 working on API games on the data from 3 kaggle datasets:
https://www.kaggle.com/datasets/mylesoneill/game-of-thrones
https://www.kaggle.com/datasets/iamsouravbanerjee/game-of-thrones-dataset
https://www.kaggle.com/datasets/ulrikthygepedersen/game-of-thrones-character-deaths

5 tables, but 2 nearly identical and only 2 with common key. Extra work to be done to link the 2 last tables

-- 1. define potential resources -- character (was 'names') -- house (not done) -- 2. potential endpoints -- /character -- /character/<name_id>

-- /house (not done) -- /house/<name_id> (not done)

-- 3. structure -- /character/<name_id> (initial focus) -- character_id -- dead_or_not -- gender (0 for Female, 1 for Male) -- value -- house -- name

-- /character by house (with or without book details) -- DateOfDeath -- character_id -- dead_or_not -- house -- in the books (nested dictionary) -- gender (0 for Female, 1 for Male) -- name
