# StateLess Passowrd Generator
Alternative to [LessPass](https://www.lesspass.com/#/) and [Spectre](https://spectre.app/) password menagers.

Generates easy to short-term memorize static passwords and is intended to be used with a proper password menager like [KeePass](https://keepass.info/).

### Issues it solves
LessPass requires you to know the login (who on earth remembers the login?) I always remember my (not so good) password and just try until I get the login right. Although LessPass is open source, I don't feel comportable feeding the login into a password generator, because if someone intercepts your connection and gets the masterpassword, they won't yet know your login.

LessPass tries to solve the wrong problem. Using password menagers shouldn't be a problem in this day and age, what needs to be solved is what happends in case you are away from your computer and can't access your KeePass database safely. My algorithm provides (or will provide) a solution to that problem.

My algorithm generates the password in the following pattern: `convertIntoPassword(hash(hash(hash(masterpassword)servicename)version))` version is a feature that allows you to change your passowrd on a website while having the same masterpassword and service name. (Equivalent of counter in LessPass)

The generated password is also easy to memorize and type over if you are manually typing it over from one device to another.
 
## Warning
As I am a noob developer, for now the security is really bad. I can't gurantee the passowrds have good entropy and you will have to copy you passwords from the commandline meaning every password will go through the clipboard history.

Also, it isn't fully standarized right now, and the exact characters and generation method might change.

I don't recomend relying on it, and compying the generated passowrds into a password menager instead. I also assume that the generated hash provides a random sequence of 0s and 1s.

Although I hide the masterpassword as it is being entered using `getpass` and copy the password to clipboard using `pyperclip` without printing it and overwrite the clipboard with `" "`, clipboard History apps such as Clipy will save the password. 

## Documentation

To generate the easy to memorize password, the hash is as a supply of random bits to generate the following:

Password pattern: `(lU0!){R4nD0mW0rD}[123ABC]`

The password has 4 secions to it, each surrounded by one of 4 types of brackets (`()[]{}<>`):

`lU0!` is a short seqence of a lowercase, uppercase, number and symbol characters to fullfill the password requirements most websites require.

`R4nD0mW0rD` is currently a concate of names&Symbols of Elements from the Periodic Table

`123456` the end is a random hex number filling the rest of the password to 32 symbols

The recomended strength is ~10^30 possible permutations, this password generator meets that requirement even with the worst odds.

Note: right now most of the security comes from the HEX at the end, which means my "easy to memorize password generator" works due to a C&V section of HEX from the hash and due to being quite long. 

> "We will need a better alg."

## Usage

! Not ready yet

## Credits

`elementWordList.json` was filtered from [Periodic-Table-JSON](https://github.com/Bowserinator/Periodic-Table-JSON)