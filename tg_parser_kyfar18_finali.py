
import telebot
from telebot import types 
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot('your_token')
text_data = ()
meaning = None
calldata = {}

@bot.message_handler(commands= ['search'])
def way_search(message):
   markup_inline = types.InlineKeyboardMarkup()
   way_all = types.InlineKeyboardButton(text = 'Искать все 👀', callback_data = 'way_all')
   way_for_price = types.InlineKeyboardButton(text = 'Искать по цене ✨', callback_data = 'way_for_price')
   way_for_description = types.InlineKeyboardButton(text = 'Искать по описанию 🎈', callback_data = 'way_for_description')
   way_for_description_and_price = types.InlineKeyboardButton(text = 'Искать по описанию и цене ⌚', callback_data = 'way_for_description_and_price')
   way_for_price_min = types.InlineKeyboardButton(text ='Искать по минимальной цене 👁‍🗨', callback_data = 'search_for_price_min')

   markup_inline.add(way_all, way_for_price, way_for_description, way_for_description_and_price,  way_for_price_min)
   bot.send_message(message.chat.id, 'Каким способом вы хотите искать?',
   reply_markup = markup_inline )


class reg:

        bel = types.InlineKeyboardButton(text="Беларусь ❤", callback_data="belarus")
        min_obl = types.InlineKeyboardButton(text="Минская ✔", callback_data="minskaya-obl")
        brst_obl = types.InlineKeyboardButton(text="Брестская 💯", callback_data="brestskaya-obl")
        gom_obl = types.InlineKeyboardButton(text="Гомельская 💡", callback_data="gomelskaya-obl")
        grodn_obl = types.InlineKeyboardButton(text="Гродненская 🎉", callback_data="grodnenskaya-obl")
        mogl_obl = types.InlineKeyboardButton(text="Могилевская 🎁", callback_data="mogilevskaya-obl")
        vitb_obl = types.InlineKeyboardButton(text="Витебская 🎊", callback_data="vitebskaya-obl")


@bot.callback_query_handler(func=lambda call: True)       
def test_t(call):
      global calldata
      calldata['way'] = call.data
      global meaning

      if calldata['way'] == 'way_all' :

       meaning = 'way_all'
       markup_inline = types.InlineKeyboardMarkup()
       markup_inline.add(reg.vitb_obl, reg.min_obl, reg.brst_obl, reg.gom_obl, reg.grodn_obl,  reg.mogl_obl, reg.bel)
       bot.send_message(call.message.chat.id, 'Выберете место для поиска',
       reply_markup = markup_inline )

      elif (calldata['way'] ==  'belarus' or calldata['way'] ==  'minskaya-obl' or calldata['way'] ==  'brestskaya-obl' or calldata['way'] ==  'gomelskaya-obl' or calldata['way'] ==  'grodnenskaya-obl' or calldata['way'] ==  'mogilevskaya-obl' or calldata['way'] ==  'vitebskaya-obl') and meaning == 'way_all':
          
           def way_all(message):
            bot.send_message(message.chat.id,'Вот что я нашел')
            query = message.text
            url1 = (f'https://www.kufar.by/l/r~{calldata["way"]}?ot=1&query={query}')
            response = requests.get(url1)
            soup = BeautifulSoup(response.text, 'html.parser')
            status = (response.status_code)
            try:
             if status == 200:
              list = soup.find('div',class_="styles_wrapper__yDu37")
              content = list.find('div',class_="styles_content__taJoq")
              conteiner = content.find('div',class_="styles_container__rDJki styles_container-children__asGHA")
              content2 = conteiner.find('div',class_="styles_listings__content__lYwC3")
              content3 = content2.find('div',class_="styles_content__right__gkEqp")
              obiava = content3.find('div',class_="styles_wrapper__G_0_A")
              obiava2 = obiava.find('div',class_="styles_cards__bBppJ")

              section = obiava2.find_all('section')

              for products in section:
   
               product = products.find('a',class_="styles_wrapper__5FoK7")
               bot.send_message(call.message.chat.id, product.text )
               links = products.find('a', class_='styles_wrapper__5FoK7').get('href') 
               bot.send_message(call.message.chat.id, links )
             elif status == 404:
               bot.send_message(call.message.chat.id, 'Не найдено' )
            except:
              bot.send_message(call.message.chat.id, 'Введите данные корректо' )

           mesg = bot.send_message(call.message.chat.id,'Напишите название товара')
           bot.register_next_step_handler(mesg,way_all)



      elif calldata['way'] == 'way_for_price' :

       meaning = 'way_for_price'
       markup_inline = types.InlineKeyboardMarkup()
       markup_inline.add(reg.vitb_obl, reg.min_obl, reg.brst_obl, reg.gom_obl, reg.grodn_obl,  reg.mogl_obl, reg.bel)
       bot.send_message(call.message.chat.id, 'Выберете место для поиска',
       reply_markup = markup_inline )
       
      elif (calldata['way'] ==  'belarus' or calldata['way'] ==  'minskaya-obl' or calldata['way'] ==  'brestskaya-obl' or calldata['way'] ==  'gomelskaya-obl' or calldata['way'] ==  'grodnenskaya-obl' or calldata['way'] ==  'mogilevskaya-obl' or calldata['way'] ==  'vitebskaya-obl') and meaning == 'way_for_price':

          def way_for_price(message):
            max_price = bot.send_message(message.chat.id,'Введите максимальную цену товара')
            global query
            query = message.text
            bot.register_next_step_handler(max_price, way_for_price_price)

          def way_for_price_price(message):
            price = message.text
            rtext = calldata['way']
            rtext2 = rtext.replace('1','')
            url1 = (f'https://www.kufar.by/l/r~{rtext2}?ot=1&query={query}')
            bot.send_message(message.chat.id,'Вот что я нашёл')
         
            response = requests.get(url1)
            status = (response.status_code)
            try:
             if status == 200:
              soup = BeautifulSoup(response.text, 'html.parser')

              list = soup.find('div',class_="styles_wrapper__yDu37")
              content = list.find('div',class_="styles_content__taJoq")
              conteiner = content.find('div',class_="styles_container__rDJki styles_container-children__asGHA")
              content2 = conteiner.find('div',class_="styles_listings__content__lYwC3")
              content3 = content2.find('div',class_="styles_content__right__gkEqp")
              obiava = content3.find('div',class_="styles_wrapper__G_0_A")
              obiava2 = obiava.find('div',class_="styles_cards__bBppJ")
              section = obiava2.find_all('section')

              for products in section:
   
                product = products.find('a',class_="styles_wrapper__5FoK7")
                links = products.find('a', class_='styles_wrapper__5FoK7').get('href') 
                styles_content_data = product.find('div',class_="styles_content__5GOlX")
                styles_top_data = styles_content_data.find('div',class_="styles_top__n9kPn")
                price_data = styles_top_data.find(class_="styles_price__G3lbO")
                price_text = (price_data.text)
                price_text2 = price_text.replace(' ', '')
                price_text3 = price_text2.replace('р.',' ')
                price_text4 = price_text3.replace('$*','')
                price_text5 = price_text4.split()[0]

                try:
                 price_text6 = float(price_text5)
                 price_text7 = round(price_text6)
                 if int(price_text7) <= float(price):
                  bot.send_message(message.chat.id,product.text)
                  bot.send_message(message.chat.id,links )
                except:
                  bot.send_message(message.chat.id,product.text)
                  bot.send_message(message.chat.id,links )

             elif status == 404:
              bot.send_message(call.message.chat.id, 'Не найдено' )
            except:
              bot.send_message(call.message.chat.id, 'Введите данные корректо' )
          mesg = bot.send_message(call.message.chat.id,'Напишите название товара')
          bot.register_next_step_handler(mesg,way_for_price)

      elif calldata['way'] == 'way_for_description' :

       meaning = 'way_for_description'
       markup_inline = types.InlineKeyboardMarkup()
       markup_inline.add(reg.vitb_obl, reg.min_obl, reg.brst_obl, reg.gom_obl, reg.grodn_obl,  reg.mogl_obl, reg.bel)
       bot.send_message(call.message.chat.id, 'Выберете место для поиска',
       reply_markup = markup_inline )

      elif (calldata['way'] ==  'belarus' or calldata['way'] ==  'minskaya-obl' or calldata['way'] ==  'brestskaya-obl' or calldata['way'] ==  'gomelskaya-obl' or calldata['way'] ==  'grodnenskaya-obl' or calldata['way'] ==  'mogilevskaya-obl' or calldata['way'] ==  'vitebskaya-obl') and meaning == 'way_for_description':

       def way_for_description(message):
            word_send_description = bot.send_message(message.chat.id,'Введите слово для поиска по описанию')
            global query
            query = message.text          
            bot.register_next_step_handler(word_send_description, way_for_description_description)

       def way_for_description_description(message):
            description_input = message.text
            rtext2 = calldata['way']
            url1 = (f'https://www.kufar.by/l/r~{rtext2}?ot=1&query={query}')
            bot.send_message(message.chat.id,'Подождите немного, Вот что я нашёл')
            response = requests.get(url1)
            status = (response.status_code)
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
             if status == 200:
               
              list = soup.find('div',class_="styles_wrapper__yDu37")
              content = list.find('div',class_="styles_content__taJoq")
              conteiner = content.find('div',class_="styles_container__rDJki styles_container-children__asGHA")
              content2 = conteiner.find('div',class_="styles_listings__content__lYwC3")
              content3 = content2.find('div',class_="styles_content__right__gkEqp")
              obiava = content3.find('div',class_="styles_wrapper__G_0_A")
              obiava2 = obiava.find('div',class_="styles_cards__bBppJ")
              section = obiava2.find_all('section')

              for products in section:
   
                 product = products.find('a',class_="styles_wrapper__5FoK7")
                 links = products.find('a', class_='styles_wrapper__5FoK7').get('href') 
                 html_data = requests.get(links)
                 html_data2 = BeautifulSoup(html_data.text, 'html.parser')
                 try:
                  try:
                   announcement_data3 = html_data2.find('div',id='__next') #<div id="__next">
                   contentt = announcement_data3.find('div',id='content') #<div id="content" 
                   announcement = contentt.find('div',class_="styles_content__main__mYAz3") #<div class="styles_content__main__mYAz3"
                   container = announcement.find('div',class_="styles_container__ohHNG") #<div class="styles_container__ohHNG">
                   styles_adview_wrapper = container.find('div',class_="styles_adview_wrapper__ccgmb") #<div class="styles_adview_wrapper__ccgmb">
                   styles_content_wrapper = styles_adview_wrapper.find('div',class_="styles_content_wrapper__YnexT") #<div class="styles_content_wrapper__YnexT">
                   styles_content_wrapper2 = styles_content_wrapper.find('div',class_="styles_adview_content__UCxmE") #<div class="styles_adview_content__UCxmE" 
                   description_block = styles_content_wrapper2.find('div',class_="styles_description__pv5CW")
                   styles_description_content =  description_block.find('div',class_="styles_description_content__raCHR") #<div class="styles_description_content__raCHR"

                   for worlddd in styles_description_content.text.split():
                     if worlddd == description_input:
                        bot.send_message(message.chat.id,product.text)
                        bot.send_message(message.chat.id,links)
                        bot.send_message(message.chat.id,styles_description_content.text)

                  except: 
                   alternative_date = html_data2.find('div',id='__next')
                   all_content = alternative_date.find('div',class_="styles_wrapper__yDu37")
                   all_content2 = all_content.find('div',class_="styles_content__taJoq")
                   all_content3 = all_content2.find('div',itemprop="description")
      
                   for worlddd  in  all_content3.text.split():
                      if worlddd == description_input:
                        bot.send_message(message.chat.id,product.text)
                        bot.send_message(message.chat.id,links)
                        bot.send_message(message.chat.id,all_content3.text)

                 except:
                   pass
             elif status == 404:
               bot.send_message(call.message.chat.id, 'Не найдено' )
            except:
              bot.send_message(call.message.chat.id, 'Введите данные корректо' )

       mesg = bot.send_message(call.message.chat.id,'Напишите название товара')
       bot.register_next_step_handler(mesg,way_for_description)


      elif calldata['way'] == 'way_for_description_and_price' :

       meaning = 'way_for_description_and_price'
       markup_inline = types.InlineKeyboardMarkup()
       markup_inline.add(reg.vitb_obl, reg.min_obl, reg.brst_obl, reg.gom_obl, reg.grodn_obl,  reg.mogl_obl, reg.bel)
       bot.send_message(call.message.chat.id, 'Выберете место для поиска',
       reply_markup = markup_inline )

      elif (calldata['way'] ==  'belarus' or calldata['way'] ==  'minskaya-obl' or calldata['way'] ==  'brestskaya-obl' or calldata['way'] ==  'gomelskaya-obl' or calldata['way'] ==  'grodnenskaya-obl' or calldata['way'] ==  'mogilevskaya-obl' or calldata['way'] ==  'vitebskaya-obl') and meaning == 'way_for_description_and_price':

        def way_for_description_and_price(message):
            word_send_description = bot.send_message(message.chat.id,'Введите слово для поиска по описанию')
            global query
            query = message.text          
            bot.register_next_step_handler(word_send_description, way_for_description_and_price_description)

        def way_for_description_and_price_description(message):           
            global description_input
            description_input = message.text
            word_send_price = bot.send_message(message.chat.id,'Введите максимальную цену товара')
            bot.register_next_step_handler( word_send_price,way_for_description_and_price_logic )

        def way_for_description_and_price_logic(message):
            price = message.text
            rtext3 = calldata['way']         
            url1 = (f'https://www.kufar.by/l/r~{rtext3}?ot=1&query={query}')
            bot.send_message(message.chat.id,'Подождите немного, Вот что я нашёл')          
            response = requests.get(url1)
            status = (response.status_code)
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
             if status == 200:          

               list = soup.find('div',class_="styles_wrapper__yDu37")
               content = list.find('div',class_="styles_content__taJoq")
               conteiner = content.find('div',class_="styles_container__rDJki styles_container-children__asGHA")
               content2 = conteiner.find('div',class_="styles_listings__content__lYwC3")
               content3 = content2.find('div',class_="styles_content__right__gkEqp")
               obiava = content3.find('div',class_="styles_wrapper__G_0_A")
               obiava2 = obiava.find('div',class_="styles_cards__bBppJ")
               section = obiava2.find_all('section')

               for products in section:
   
                product = products.find('a',class_="styles_wrapper__5FoK7")
                links = products.find('a', class_='styles_wrapper__5FoK7').get('href') 
                styles_content_data = product.find('div',class_="styles_content__5GOlX")
                styles_top_data = styles_content_data.find('div',class_="styles_top__n9kPn")
                price_data = styles_top_data.find(class_="styles_price__G3lbO")

                price_text = (price_data.text)
                price_text2 = price_text.replace(' ', '')
                price_text3 = price_text2.replace('р.',' ')
                price_text4 = price_text3.replace('$*','')
                price_text5 = price_text4.split()[0]

                try:
                 price_text6 = float(price_text5)
                 price_text7 = round(price_text6)                 
                 if price_text7 <= float(price):
                  gh = links
                  html_data = requests.get(gh)
                  html_data2 = BeautifulSoup(html_data.text, 'html.parser')
                  try:
                    try:
                     announcement_data3 = html_data2.find('div',id='__next') #<div id="__next">
                     contentt = announcement_data3.find('div',id='content') #<div id="content" 
                     announcement = contentt.find('div',class_="styles_content__main__mYAz3") #<div class="styles_content__main__mYAz3"
                     container = announcement.find('div',class_="styles_container__ohHNG") #<div class="styles_container__ohHNG">
                     styles_adview_wrapper = container.find('div',class_="styles_adview_wrapper__ccgmb") #<div class="styles_adview_wrapper__ccgmb">
                     styles_content_wrapper = styles_adview_wrapper.find('div',class_="styles_content_wrapper__YnexT") #<div class="styles_content_wrapper__YnexT">
                     styles_content_wrapper2 = styles_content_wrapper.find('div',class_="styles_adview_content__UCxmE") #<div class="styles_adview_content__UCxmE" 
                     description_block = styles_content_wrapper2.find('div',class_="styles_description__pv5CW")
                     styles_description_content =  description_block.find('div',class_="styles_description_content__raCHR") #<div class="styles_description_content__raCHR"

                     for worlddd in styles_description_content.text.split():
                      if worlddd == description_input:
                        bot.send_message(message.chat.id,product.text)
                        bot.send_message(message.chat.id,links)
                        bot.send_message(message.chat.id,styles_description_content.text)

                    except: 
                      alternative_date = html_data2.find('div',id='__next')
                      all_content = alternative_date.find('div',class_="styles_wrapper__yDu37")
                      all_content2 = all_content.find('div',class_="styles_content__taJoq")
                      all_content3 = all_content2.find('div',itemprop="description")
      
                      for worlddd  in  all_content3.text.split():
                       if worlddd == description_input:
                        bot.send_message(message.chat.id,product.text)
                        bot.send_message(message.chat.id,links)
                        bot.send_message(message.chat.id,all_content3.text)

                  except:
                    pass
                except: 
                 pass
             elif status == 404:
               bot.send_message(message.chat_id,'Не найдено')
            except:
              bot.send_message(message.chat_id,'Введите корректно данные')    

        mesg = bot.send_message(call.message.chat.id,'Напишите название товара')
        bot.register_next_step_handler(mesg,way_for_description_and_price)

      elif calldata['way'] == 'search_for_price_min' :
       
       meaning = 'search_for_price_min'
       markup_inline = types.InlineKeyboardMarkup()
       markup_inline.add(reg.vitb_obl, reg.min_obl, reg.brst_obl, reg.gom_obl, reg.grodn_obl,  reg.mogl_obl, reg.bel)
       bot.send_message(call.message.chat.id, 'Выберете место для поиска',
       reply_markup = markup_inline )

      elif (calldata['way'] ==  'belarus' or calldata['way'] ==  'minskaya-obl' or calldata['way'] ==  'brestskaya-obl' or calldata['way'] ==  'gomelskaya-obl' or calldata['way'] ==  'grodnenskaya-obl' or calldata['way'] ==  'mogilevskaya-obl' or calldata['way'] ==  'vitebskaya-obl') and meaning == 'search_for_price_min':

        def way_for_min_price(message):
            max_price = bot.send_message(message.chat.id,'Введите минимальную цену товара')
            global query
            query = message.text
            bot.register_next_step_handler(max_price, way_for_min_price_price)

        def way_for_min_price_price(message):
            min_price = message.text
            rtext = calldata['way']
            rtext2 = rtext.replace('4','')
            url1 = (f'https://www.kufar.by/l/r~{rtext2}?ot=1&query={query}')
            bot.send_message(message.chat.id,'Вот что я нашёл')
         
            response = requests.get(url1)
            status = (response.status_code)
            try:
             if status == 200:
              soup = BeautifulSoup(response.text, 'html.parser')

              list = soup.find('div',class_="styles_wrapper__yDu37")
              content = list.find('div',class_="styles_content__taJoq")
              conteiner = content.find('div',class_="styles_container__rDJki styles_container-children__asGHA")
              content2 = conteiner.find('div',class_="styles_listings__content__lYwC3")
              content3 = content2.find('div',class_="styles_content__right__gkEqp")
              obiava = content3.find('div',class_="styles_wrapper__G_0_A")
              obiava2 = obiava.find('div',class_="styles_cards__bBppJ")
              section = obiava2.find_all('section')

              for products in section:
   
                product = products.find('a',class_="styles_wrapper__5FoK7")
                links = products.find('a', class_='styles_wrapper__5FoK7').get('href') 
                styles_content_data = product.find('div',class_="styles_content__5GOlX")
                styles_top_data = styles_content_data.find('div',class_="styles_top__n9kPn")
                price_data = styles_top_data.find(class_="styles_price__G3lbO")
                price_text = (price_data.text)
                price_text2 = price_text.replace(' ', '')
                price_text3 = price_text2.replace('р.',' ')
                price_text4 = price_text3.replace('$*','')
                price_text5 = price_text4.split()[0]
                
                try:
                 price_text6 = float(price_text5)
                 price_text7 = round(price_text6)
                 if price_text7 >= float(min_price):
                  bot.send_message(message.chat.id,product.text)
                  bot.send_message(message.chat.id,links )                 
                except:
                  bot.send_message(message.chat.id,product.text)
                  bot.send_message(message.chat.id,links )

             elif status == 404:
              bot.send_message(call.message.chat.id, 'Не найдено' )

            except:
              bot.send_message(call.message.chat.id, 'Введите данные корректо' )
        mesg = bot.send_message(call.message.chat.id,'Напишите название товара')
        bot.register_next_step_handler(mesg,way_for_min_price)
 


bot.polling(none_stop=True)
