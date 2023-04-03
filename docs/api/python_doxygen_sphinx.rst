Slash Commands
==============

.. py:method:: info()
   
      Displays some information about the bot.

      .. code-block:: none
   
            Usage: /info

.. py:method:: commands()
   
      Displays a list of all commands.

      .. code-block:: none
   
            Usage: /commands

.. py:method:: add_event(name, date, time)
      
         Adds an event to the database.

         * name: The name of the event.
         * date: The date of the event. Format: DDMMYYYY
         * time: The time of the event. Format: HHMM
   
         .. code-block:: none
      
               Usage: /add_event <name> <date> <time>
            
               Example: /add_event "My Event" "01012020" "2342"

.. py:method:: remove_event(name)

         Removes an event from the database.

         * name: The name of the event.

         .. code-block:: none
      
               Usage: /remove_event <name>
            
               Example: /remove_event "My Event"

.. py:method:: list_events()
   
            Lists all events in the database.
   
            .. code-block:: none
         
                  Usage: /list_events
            
      