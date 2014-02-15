import win32ui
import dde


def SendCommandToGame(command,ExpectedResult=False):
    """
    This function sends a CAOS command to a C1 or C2 game and returns the result
    You have to specify whether or not the executed command expects output to be returned, as both kinds of commands require different calls
    """
    server = dde.CreateServer()
    server.Create("TestClient") # This can be anything or even empty.
    conversation = dde.CreateConversation(server)

    conversation.ConnectTo("Vivarium", "Anything") # Creatures DDE application is "Vivarium", yours can be anything.
    conversation.Poke("Macro", command+"\x00") # Rembember Creature expects C-style \0 terminated strings as DDE inputs
    if ExpectedResult==True:
        # If the command returns a result use the Request() method
        rep=conversation.Request("Macro")
    else:
        # If the command doesn't a result use the exec() method
        conversation.Exec(command+"\x00")
        rep=""
    server.Destroy()
    return rep


# Now we can run arbitrary CAOS commands :
print SendCommandToGame("dde: getb cnam",True)
