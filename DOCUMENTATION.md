# Strings

Only `'` character is allowed at this time  
Format is not implemented at this time  
Can't use things like `\n` at the moment

Example : `'Thats a string'`

# Numbers

it's literally a number, like : `14`

# Variables

Use `let` or `var` keyword to assign your variables  
Example : `let name = 'ENDERastronaute'`

# If Elif Else statements

Unlike python it uses `{}`  
`or` and `and` are not implemented yet

Example : `if name == 'ENDERastronaute' { log(name) }`

# Basic functions

here are the basic functions of PySQL :

1. `log()` Write text to terminal  
   Example : `log('Hello World')`
2. `input()` Read text from terminal  
   Example : `let name = input('What's your name ? ')`

# SQL requests (yipeee)

So, PySQL has 'SQL' in it, here goes the part :  
SQL requests have an HTML like style (<><>).

SQL requests can be done only for PostgreSQL at the moment.

Example :

```SQL
<SQL>
   SELECT * FROM client
   ORDER BY name
<user 'postgres', pwd 'postgres', host '127.0.0.1', port 5432, db 'database'>
```

For now (this will soon be more efficient) you'll need to specify the user, password, host, port and database between the final <>.

# Custom functions

You can't create your own functions yet

    <(^)
     /()\ PySQL
      --
