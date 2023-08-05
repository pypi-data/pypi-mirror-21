microquest - CLI to gamify anything

# installation

	pip install microquest

# usage

the following asciicast does not reflect the current state of the game but will give you a hint of how it could be used:

[![asciicast](https://asciinema.org/a/7yar4jllfpm9hsgn5yom6kr16.png)](https://asciinema.org/a/7yar4jllfpm9hsgn5yom6kr16)


	Usage: mq [OPTIONS] COMMAND [ARGS]...

	Options:
	  --help  Show this message and exit.

	Commands:
	  init      init the game
	  importq   import a quest file

	  quests    print quests
	  add       add a quest
	  rm        remove a quest

	  do        do a quest
	  skip      skip a quest
	  buy       buy something (negative value quest)

	  complete  complete a quest, remove it
	  fail      fail a quest, remove it

	  log       print log
	  status    get player status

	  table     print xp table

# halp

add some sample quests with `mq importq quest-samples.ini`

add bash completions with `source completion.sh`

shop items are represented as negative value quests, use buy action.

# how to integrate with git

do not run those commands blindly:

	mkdir -p ~/.git_templates/hooks
	echo "mq do commit" > ~/.git_templates/hooks/post-commit
	echo "mq do push" > ~/.git_templates/hooks/pre-push
	chmod +x ~/.git_templates/hooks/*
	git config --global init.templatedir '~/.git_templates'
	mq add commit "git commit"
	mq add push "git push" 80

then do git init in every of your repository to add the local hooks

# ideas

* you have too much privacy? microblog your progress! the logfile in `~/.config/microquest/log` is compatible with [twtxt](https://github.com/buckket/twtxt)
* share you quests files among a team

	
# todo

* add silent mode for hooks
* --charfile option
* 1 log per char
