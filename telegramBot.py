import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json
import cherrypy

class CONFIGURATION:
    def __init__(self):
        with open('telegramBot_config.json','r') as conf:
            self.token = json.load(conf)["token"]

class RESTAPI:
    exposed=True
    def __init__(self, token):
        self.token = token
        self.bot = telepot.Bot(token)
        self.chatIDs=[]
        MessageLoop(self.bot, {'chat': self.on_chat_message,
                  'callback_query': self.on_callback_query}).run_as_thread()
        
    def alert_menu_keyboard(self):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text='Call him/her', callback_data='friend')],
                            [InlineKeyboardButton(text='Call Police', callback_data='police')]
                        ])
        return keyboard    
    
    def on_chat_message(self,msg):
        content_type, chat_type, chat_id = telepot.glance(msg)       
        message = msg['text']
        if message=="/start":
            self.chatIDs.append(chat_id)
            self.bot.sendMessage(chat_id, text="Service is activated\nYou would be notified when your friend is driving sleepy\nYou can stop receiving notifications by using /stop")
        if message=="/stop":
            self.bot.sendMessage(chat_id, text="You will be no longer notified. use /start to re-activate the service")
            self.chatIDs.remove(chat_id)
            
    def on_callback_query(self,msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        if query_data=="friend":
            self.bot.sendMessage(from_id, text=f'{self.jsonBody["Phone"]}')
        elif query_data=="police":
            self.bot.sendMessage(from_id, text="911")

    def POST(self,*uri):
        tosend=None
        output={"status":"not-sent","message":tosend}
        if len(uri)!=0:
            if uri[0]=='alert':
                body=cherrypy.request.body.read()
                self.jsonBody=json.loads(body)
                tosend='Your friend {} needs your help!\non {} we think he/she is sleepy while driving.'.format(self.jsonBody["Name"],self.jsonBody["timeStamp"] )
                output={"status":"sent","message":tosend}
                for chat_ID in self.chatIDs:
                    self.bot.sendMessage(chat_ID, text=tosend , reply_markup=self.alert_menu_keyboard())
            else:
                tosend = None
        return json.dumps(output)



if __name__ == "__main__":
    cherryConf={
		'/':{
				'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
				'tool.session.on':True
		}
	}	
    bot=RESTAPI(CONFIGURATION().token)
    cherrypy.tree.mount(bot,'/',cherryConf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8282})
    cherrypy.engine.start()
    cherrypy.engine.block()

