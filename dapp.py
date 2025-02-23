import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup,KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.inline_keyboard import InlineKeyboardButton,InlineKeyboardMarkup

conn = sqlite3.connect('darkmovieuz.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS userid (id INTEGER PRIMARY KEY, user_id INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, code TEXT, title TEXT, video TEXT)''')



cursor.execute("""CREATE TABLE IF NOT EXISTS saved_movies (id INTEGER PRIMARY KEY , user_id INTEGER , movie_code INTEGER )""")


conn.commit()


bot_token = "6661989497:AAHrH7urHD01RjXUlis7DU6pmmgHXOn186k"
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["pan"],state="*")
async def pane(message:types.Message,state:FSMContext):
    await message.answer("Panel bo'limiga kirish uchun parol kiriting !")
    await state.finish()
    await state.set_state("par")



@dp.message_handler(state="par")
async def panel(msg:types.Message,state:FSMContext):

    passw = msg.text

    parol = "pythonchiakang03"

    if passw == parol:
        global usering
        usering = msg.from_user.id
        panellar=ReplyKeyboardMarkup(
            keyboard=[
            ["📊Statistika",
                "➕Kanal qo'shish"],
                ["📽Kino qo'shish",
                "⛔️Kanal o'chirish"], 
                [ "📣Kanallar ro'yxati",
                 "🔗Forward xabar"],
                ["⚪️Inline Xabar",
                "🔙Ortga"]  
            ],resize_keyboard=True
        )
        await msg.answer("Adminlik tasdiqlandi!")
        await msg.answer("⬇️<b>Kerakli bo'limni tanlang</b>⬇️",reply_markup=panellar,parse_mode="HTML")
        await state.set_state("panel")

    else:
        await msg.answer("Siz admin emassiz!")
        await state.finish()
        

import re
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, MessageToForwardNotFound

@dp.message_handler(text="🔗Forward xabar", state="*")
async def forwardmes(fmessage: types.Message, state: FSMContext):
    await fmessage.answer("Xabarni havola linki yoki raqamini yuboring!")
    await state.set_state("fmes")

@dp.message_handler(state="fmes")
async def fmes(fmes: types.Message, state: FSMContext):
    try:
        f_mes = int(fmes.text)  # Foydalanuvchidan olingan raqam
    except ValueError:
        await fmes.answer("Iltimos, to'g'ri xabar raqamini kiriting!")
        return

    yetkazilganlar = 0
    yetkazilmaganlar = 0
    blok_qilganlar = 0  # Blok qilgan foydalanuvchilar soni

    cursor.execute("SELECT DISTINCT user_id FROM userid")
    user_ids = cursor.fetchall()

    for user_id in user_ids:
        try:
            await bot.forward_message(
                chat_id=user_id[0], 
                from_chat_id='@sjsksnsbsh', 
                message_id=f_mes
            )
            yetkazilganlar += 1
        except BotBlocked:
            blok_qilganlar += 1
        except MessageToForwardNotFound:
            await fmes.answer("Berilgan xabarni topib bo'lmadi.")
            return
        except ChatNotFound:
            yetkazilmaganlar += 1
        except Exception as e:
            print(f"Error: {e}")
            yetkazilmaganlar += 1

    await fmes.answer(
        f"<b>Xabar foydalanuvchilarga muvaffaqiyatli yuborildi!</b>✅\n\n"
        f"🚀 Yetkazildi : <b>{yetkazilganlar}</b> ta\n"
        f"🛑 Yetkazilmadi : <b>{yetkazilmaganlar}</b> ta\n"
        f"❌ Blok qilganlar : <b>{blok_qilganlar}</b> ta",
        parse_mode="HTML"
    )
    
    await state.finish()



#############################
@dp.callback_query_handler(lambda r:r.data=="radq",state="*")
async def radq(call:types.CallbackQuery,state:FSMContext):
    qabul = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tasdiqlanmadi❌", callback_data='radq')]
        ]
    )
    await call.message.edit_reply_markup(reply_markup=qabul)
    await call.answer("Post joylanmadi!❌", show_alert=True)
    await state.finish()


###########################




#Kanallar royxati
@dp.message_handler(text="📣Kanallar ro'yxati", state="*")
async def channel_dic(msg: Message, state: FSMContext):
    kanal_names = []

    if CHANNEL_URLS:
        for channel_url in CHANNEL_URLS:
            kanal_name = channel_url.replace("https://t.me/", "@")
            kanal_names.append(kanal_name)

        channels_str = "\n".join(kanal_names)

        message = f"<b>Bazadagi Kanallar ro'yxati</b>\n{channels_str}"
        await msg.answer(message, parse_mode="HTML")
    else:
        await msg.answer("Kanal topilmadi.")
       

@dp.message_handler(text="📽Kino qo'shish",state="*")
async def kinoadd(msg:types.Message,state:FSMContext):
    tugatish = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tugatish",callback_data="tugat")]
        ],row_width=2
    )
    await msg.answer("<b>Kino qoshish uchun kodini kirting!</b>",parse_mode="HTML",reply_markup=tugatish)
    await state.finish()
    await state.set_state("kodliadd")

@dp.message_handler(state="kodliadd",content_types=types.ContentTypes.ANY)
async def orr(msg:Message,state:FSMContext):

    global umum_kino
    umum_kino=(msg.text)
    tugatish = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tugatish",callback_data="tugat")]
        ],row_width=2
    )
    if umum_kino:
        await msg.answer("<b>Kinosining izohini yuboring!</b>",parse_mode="HTML",reply_markup=tugatish)
        await state.finish()
        await state.set_state("cinema_izoh")
    else:
        await msg.answer("Iltimos raqam orqali kod kiriting")

@dp.message_handler(state="cinema_izoh",content_types=types.ContentTypes.TEXT)
async def izoh(msg:Message,state:FSMContext):
    global k_izoh
    k_izoh=msg.text
    tugatish = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tugatish",callback_data="tugat")]
        ],row_width=2
    )
    await msg.answer("<b>Video yuboring!</b>",parse_mode="HTML",reply_markup=tugatish)
    await state.finish()
    await state.set_state("vvv")

@dp.message_handler(state="vvv",content_types=types.ContentTypes.VIDEO)
async def vvv(msg:Message,state:FSMContext):
    modd=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Davom etish",callback_data='next1')],
            [InlineKeyboardButton(text="Tugatish",callback_data='end1')]
        ],row_width=2
    )
    vd=msg.video
    file_id=vd.file_id
    conn = sqlite3.connect('darkmovieuz.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO data (code,title, video) VALUES (?, ?,?)", (umum_kino, k_izoh,file_id))
    conn.commit()

    cursor.close()
    conn.close()
    await state.finish()
    await msg.answer("Kino qo'shildi!",reply_markup=modd)
    await state.set_state('next1')


@dp.callback_query_handler(lambda c:c.data=="next1",state="next1")
async def next(cal:types.CallbackQuery,state:FSMContext):
    await state.finish()
    await kinoadd(cal.message,state)
    
@dp.callback_query_handler(lambda d:d.data=="end1",state="next1")
async def end(cal:types.CallbackQuery,state:FSMContext):
    await state.finish()
    await start(cal.message,state)





#Xabar yuborish


@dp.message_handler(text="⚪️Inline Xabar",state="*")
async def inline_xabar(message:types.Message,state:FSMContext):
    tugatish = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tugatish",callback_data="tugat")]
        ],row_width=2
    )

    await message.answer("Xabaringiz qoldiring!",reply_markup=tugatish)
    await state.finish()
    await state.set_state("send_message")

@dp.message_handler(state="send_message",content_types=types.ContentTypes.TEXT)
async def send_message(message:types.Message,state:FSMContext):
    tugatish = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tugatish",callback_data="tugat")]
        ],row_width=2
    )
    global xabar1
    xabar1 = message.text
    await message.answer("Inline tugma uchun link yuboring!",reply_markup=tugatish)
    await state.finish()
    await state.set_state("link")


@dp.message_handler(state="link")
async def link(message:types.Message,state:FSMContext):
    tugatish = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tugatish",callback_data="tugat")]
        ],row_width=2
    )
    global linkk;
    linkk = message.text
    if "https:" in linkk:
        await message.answer("Inline tugma uchun nom bering ! ",reply_markup=tugatish)
        await state.finish()
        await state.set_state("inline_nom")
    else:
        await message.answer("Linkda xatolik")


@dp.message_handler(state="inline_nom")
async def inline_name(message:types.Message,state:FSMContext):
    global inline_nom
    inline_nom = message.text
    inline_send = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{inline_nom}",url=f"{linkk}")],
            [InlineKeyboardButton(text="Yuborish",callback_data="send"),
             InlineKeyboardButton(text="Rad qilish",callback_data="nosend")]
        ],row_width=2
    )
    await message.answer(f"{xabar1} \n\nUshbu xabarni yuborasizmi?",reply_markup=inline_send)
    await state.finish()
    await state.set_state("yuborish")

@dp.callback_query_handler(lambda d:d.data=="send",state="*")
async def send_inline(query:types.CallbackQuery,state:FSMContext):
    yetkazilganlarr=0
    yetkazilmaganlar=0
    inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{inline_nom}", url=f"{linkk}")]
        ],
        row_width=2
    )
    cursor.execute("SELECT DISTINCT user_id FROM userid")
    user_ids = cursor.fetchall()

    for user_id in user_ids:
        try:
            await bot.send_message(user_id[0], xabar1,reply_markup=inline,parse_mode="HTML")
            yetkazilganlarr=+1
        except Exception as e:
            logging.error(f"Error sending message to user {user_id[0]}: {e}")
            yetkazilmaganlar+=1

    await query.message.answer(
        f"<b>Xabar foydalanuvchilarga muvaffaqiyatli yuborildi!</b>✅\n\n"
        f"🚀Yetkazildi : <b>{yetkazilganlarr}</b> ta\n"
        f"🛑Yetkazilmadi : <b>{yetkazilmaganlar}</b> ta",
        parse_mode="HTML"
    )
    await state.finish()

@dp.callback_query_handler(lambda u:u.data=="nosend",state="*")
async def nosend(call:types.CallbackQuery,state:FSMContext):
    await call.message.delete()
    await state.finish()


#Rasm inline xabar
    
@dp.message_handler(content_types=types.ContentType.PHOTO, state="send_message")
async def send_xabar(msg: types.Message, state: FSMContext):
    tugatish = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tugatish",callback_data="tugat")]
        ],row_width=2
    )
    global photot
    photot = msg.photo[-1].file_id
    await msg.answer("<b>✍️Rasmning izohini qoldiring</b>", parse_mode="HTML",reply_markup=tugatish)
    await state.set_state('Rasm_izoh')

@dp.message_handler(state="Rasm_izoh")
async def rasm(msg: types.Message, state: FSMContext):
    tugatish = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tugatish",callback_data="tugat")]
        ],row_width=2
    )
    global izohh
    izohh = msg.text

    await msg.answer("Inline tugma uchun link yuboring !",reply_markup=tugatish)
    await state.finish()
    
    await state.set_state("rasm_inline_link")

@dp.message_handler(state="rasm_inline_link")
async def rasm_inline(message:types.Message,state:FSMContext):
    tugatish = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tugatish",callback_data="tugat")]
        ],row_width=2
    )
    global rasm_link
    rasm_link = message.text
    if "https:" in rasm_link:
        await message.answer("Inline tugma uchun nom kiriting !",reply_markup=tugatish)
        await state.finish()
        await state.set_state("rasminline_nom")
    else:
        await message.answer("Linkda xatolik")

@dp.message_handler(state="rasminline_nom")
async def rasm_nom(message:types.Message,state:FSMContext):
    global rasm_nomi
    rasm_nomi = message.text
    yubor = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{rasm_nomi}",url=f"{rasm_link}")],
            [InlineKeyboardButton(text="Yuborish", callback_data="raketaa"),
             InlineKeyboardButton(text="Rad qilish", callback_data="uchma")]
        ], row_width=2
    )
    await message.answer_photo(photo=photot, caption=f"{izohh} \n\n Ushbu xabarni yuborasizmi? ",reply_markup=yubor)
    await state.finish()
    await state.set_state("jonatish")

@dp.callback_query_handler(lambda c: c.data == "raketaa", state="*")
async def izoh_pho(call: types.CallbackQuery, state: FSMContext):
    bordi = 0
    bormadi = 0
    inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{rasm_nomi}", url=f"{rasm_link}")]
        ],
        row_width=2
    )

    cursor.execute("SELECT DISTINCT user_id FROM userid")
    user_ids = cursor.fetchall()

    for user_id in user_ids:
        try:
            await bot.send_photo(user_id[0], photo=photot, caption=izohh, reply_markup=inline,parse_mode="HTML")
            bordi += 1
        except Exception as e:
            logging.error(f"Error sending message to user {user_id[0]}: {e}")
            bormadi += 1

    await call.message.answer(f"<b>Xabar foydalanuvchilarga muvaffaqiyatli yuborildi!</b>✅\n\n"
                              f"🚀Yetkazildi : <b>{bordi}</b> ta\n🛑Yetkazilmadi : <b>{bormadi}</b> ta",
                              parse_mode="HTML")

    await state.finish()

@dp.callback_query_handler(lambda u:u.data=="uchma",state="*")
async def uchma(call:types.CallbackQuery,state:FSMContext):
    await call.message.delete()
    await state.finish()

#Tugatish
    

#Video xabar inline
    
@dp.message_handler(content_types=types.ContentType.VIDEO, state="send_message")
async def send_xabar_video(msg: types.Message, state: FSMContext):
    tugatish = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tugatish",callback_data="tugat")]
        ],row_width=2
    )
    global videop
    videop = msg.video.file_id
    await msg.answer("<b>✍️Videoning izohini qoldiring</b>", parse_mode="HTML",reply_markup=tugatish)
    await state.set_state('Video_izoh')

@dp.message_handler(state="Video_izoh")
async def video(msg: types.Message, state: FSMContext):
    tugatish = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tugatish",callback_data="tugat")]
        ],row_width=2
    )
    global v_izohh
    v_izohh = msg.text

    await msg.answer("Inline tugma uchun link yuboring !",reply_markup=tugatish)
    await state.finish()
    
    await state.set_state("video_inline_link")

@dp.message_handler(state="video_inline_link")
async def video_inline(message:types.Message,state:FSMContext):
    tugatish = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tugatish",callback_data="tugat")]
        ],row_width=2
    )
    global video_link
    video_link = message.text
    if "https:" in video_link:
        await message.answer("Inline tugma uchun nom kiriting !",reply_markup=tugatish)
        await state.finish()
        await state.set_state("videoinline_nom")
    else:
        await message.answer("Linkda xatolik")
        
@dp.message_handler(state="videoinline_nom")
async def rasm_nom(message:types.Message,state:FSMContext):
    global video_nomi
    video_nomi = message.text
    yubor = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{video_nomi}",url=f"{video_link}")],
            [InlineKeyboardButton(text="Yuborish", callback_data="raketaaa"),
             InlineKeyboardButton(text="Rad qilish", callback_data="uchmaaa")]
        ], row_width=2
    )
    await message.answer_video(video=videop, caption=f"{v_izohh} \n\n Ushbu xabarni yuborasizmi? ",reply_markup=yubor)
    await state.finish()
    await state.set_state("jonatish2")

@dp.callback_query_handler(lambda c: c.data == "raketaaa", state="*")
async def izoh_vid(call: types.CallbackQuery, state: FSMContext):
    bordi = 0
    bormadi = 0
    inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{video_nomi}", url=f"{video_link}")]
        ],
        row_width=2
    )

    cursor.execute("SELECT DISTINCT user_id FROM userid")
    user_ids = cursor.fetchall()

    for user_id in user_ids:
        try:
            await bot.send_video(user_id[0], video=videop, caption=v_izohh, reply_markup=inline,parse_mode='HTML')
            bordi += 1
        except Exception as e:
            logging.error(f"Error sending message to user {user_id[0]}: {e}")
            bormadi += 1

    await call.message.answer(f"<b>Xabar foydalanuvchilarga muvaffaqiyatli yuborildi!</b>✅\n\n"
                              f"🚀Yetkazildi : <b>{bordi}</b> ta\n🛑Yetkazilmadi : <b>{bormadi}</b> ta",
                              parse_mode="HTML")

    await state.finish()

@dp.callback_query_handler(lambda t:t.data=="tugat",state="*")
async def tugat(query:types.CallbackQuery,state:FSMContext):
    await query.message.delete()
    await state.finish()

@dp.callback_query_handler(lambda u:u.data=="uchmaaa",state="*")
async def uchma(call:types.CallbackQuery,state:FSMContext):
    await call.message.delete()
    await state.finish()
 
#Kanal qoshish



CHANNEL_IDS=[]
CHANNEL_URLS=[]

@dp.message_handler(text="➕Kanal qo'shish",state="*")
async def kan(msg:Message,state:FSMContext):
    await msg.answer("""
<i>Kanal qoshish uchun kanal id raqam yuboring! \n<b>Eslatma!</b>\nKanalning id raqamini @GetAnyTelegramIdBot⬅️ ushbu botdan olishingiz mumkin! 
\nBotga start berasiz va Kanalingiz url(silka)sini yuborasiz </i>""",parse_mode="HTML")
    await state.set_state("kanal")
    


@dp.message_handler(state="kanal")
async def kanal(msg:types.Message,state:FSMContext):
    
    kanal_id = msg.text

    if kanal_id.startswith("-100"):
        CHANNEL_IDS.append(kanal_id)
        await msg.answer("<i>Kanal url silkasini yuboring!</i>", parse_mode="HTML")
        await state.set_state("url")
    elif kanal_id == "📊Statistika":
        await statistika(msg, state)
    elif kanal_id == "⛔️Kanal o'chirish":
        await delet(msg, state)
    elif kanal_id == "➕Kanal qo'shish":
        await kan(msg, state)
    elif kanal_id == "⚪️Inline Xabar":
        await xabar(msg, state)
    elif kanal_id == "📽Kino qo'shish":
        await kinoadd(msg, state)
    
    else:
        await msg.answer("❌Xato. Kanal id bunday korinishda bo'lmaydi. Qayta urining!")

@dp.message_handler(state="url")
async def url(msg:Message,state:FSMContext):
    kanal_url=msg.text
    
    urls="https:"
    if urls in kanal_url:
        CHANNEL_URLS.append(kanal_url)
        await msg.answer("<b>Kanal muvaffaqiyatli qoshildi!</b>✅",parse_mode="HTML")
    elif kanal_url=="📊Statistika":
        await statistika(msg,state)
    elif kanal_url=="⛔️Kanal o'chirish":
        await delet(msg,state)
    elif kanal_url=="⚪️Inline Xabar":
        await xabar(msg,state)
    elif kanal_url=="📽Kino qo'shish":
        await kinoadd(msg,state)
    
    else:
        await msg.answer("❌Xato. Kanal silkasi to'g'ri ekanligini tekshriring!")


#kanal o'chirish
@dp.message_handler(text="⛔️Kanal o'chirish",state="*")
async def delet(msg:types.Message,state:FSMContext):
    await msg.answer("<i>❗️Kanal id sini jonating</i>",parse_mode="HTML")
    await state.set_state("del")

@dp.message_handler(state="del")
async def dele(msg:types.Message,state:FSMContext):
    global k_id
    k_id=msg.text
    if k_id=="📊Statistika":
        await statistika(msg,state)
    elif k_id=="⚪️Inline Xabar":
        await xabar(msg,state)
    elif k_id=="➕Kanal qo'shish":
        await kan(msg,state)
    elif k_id=="📽Kino qo'shish":
        await kinoadd(msg,state)
    elif k_id=="🔙Ortga":
        await pane(msg,state)
    elif "-100" in k_id: 
        await msg.answer("<i>❗️Kanal silkasini jonating</i>",parse_mode="HTML")
        await state.set_state("silka")
    else:
        await msg.answer("❌Xato. Kanal id bunday korinishda bo'lmaydi. Qayta urining!")


@dp.message_handler(state="silka")
async def delete(msg:types.Message,state:FSMContext):
    global sil
    sil=msg.text
    if "https" in sil  and k_id in CHANNEL_IDS and sil in CHANNEL_URLS:
        CHANNEL_IDS.remove(k_id)
        CHANNEL_URLS.remove(sil)      
        await msg.answer("<b>Kanal muvaffaqiyatli o'chirildi✅</b>",parse_mode="HTML")
        await state.finish()
    elif sil=="📊Statistika":
        await statistika(msg,state)  
    elif k_id=="⚪️Inline Xabar":
        await xabar(msg,state)
    elif sil=="➕Kanal qo'shish":
        await kan(msg,state)
    elif sil=="📽Kino qo'shish":
        await kinoadd(msg,state)   
    else:
        await msg.answer("Bunday kanal yoq")





#Kino yangiliklari
@dp.message_handler(text="📨Kino yangiliklari",state="*")
async def cinema_new(msg:types.Message,state:FSMContext):
    foto="https://static3.tgstat.ru/channels/_0/ca/caeb424e0581c1e34c217668dd7d6f39.jpg"
    caption="🌐<b>Kino yangiliklari ushbu tugma ostida⤵️</b>"
    new=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📨Kino yangiliklari",callback_data="new",url="https://t.me/my_portfolio_py")]
        ]
    )
    await msg.answer_photo(photo=foto,caption=caption,reply_markup=new,parse_mode="HTML")
    await state.finish()


#Ortga
@dp.message_handler(text="🔙Ortga",state="*")
async def xabar(msg:Message,state:FSMContext):
    await state.finish()
    await start(msg,state)

# KINO_ZAKAZ="-1001936444889"
@dp.message_handler(text="🛒Kino Zakaz", state="*")
async def zakaz(msg: types.Message, state: FSMContext):
    nazad=ReplyKeyboardMarkup(
        keyboard=[
            ["🔙Ortga"]
        ],resize_keyboard=True
    )
    global user_iddd
    user_iddd = msg.from_user.id
    await msg.answer(
        f"Assalomu alaykum <b>{msg.from_user.first_name}</b>. \n\n<i>Kino zakaz berish uchun odob saqlagan holda o'z zakazingizni yozib qoldiring</i>!✍️",
        parse_mode="HTML",reply_markup=nazad)
    await state.set_state("zakaz")


@dp.message_handler(state="zakaz")
async def z(msg: types.Message, state: FSMContext):
    chat_id = "-1001945125076"
    global zakazz
    ort=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Bosh sahifa",callback_data="boshiga")]
        ],row_width=2
    )
    zakazz = msg.text
    bb=msg.from_user.id
    zak = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data='tasdiqlandi'),
             InlineKeyboardButton(text="❌ Rad etish", callback_data='rad')]
        ],
        row_width=2
    )
    if zakazz=="🔙Ortga" or zakazz=="/start":
        await state.finish()
        await start(msg,state)
    else:
        await bot.send_message(chat_id=chat_id, text=f"{bb}\nushbu chat egasidan zakaz keldi \n\n{zakazz}", reply_markup=zak, parse_mode="Markdown")
        await state.set_state('admin_zakaz')
        await state.finish()
        await msg.answer("<b>Zakaz adminga yuborildi</b>✅\n\n<i>Tez orada sizga admin tomonidan xabar keladi.</i> \t\t\t\t<b>Kuting</b>❗️",
                    parse_mode="HTML",reply_markup=ort)


@dp.callback_query_handler(lambda d:d.data=="boshiga")
async def boshiga(call:types.CallbackQuery,state:FSMContext):
    await call.message.delete()
    await state.finish()
    await start(call.message,state)


# Zakaz qabul qilish
@dp.callback_query_handler(lambda z: z.data == "tasdiqlandi")
async def ad_z(call: types.CallbackQuery, state: FSMContext):
    uzz=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🙋‍♂️Yana zakaz bor",callback_data="yan_z")],
            [InlineKeyboardButton(text="😊Rahmat",callback_data="rahmat_z")]

        ],row_width=2
    )
    qabul = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tasdiqlandi✅", callback_data='tasdiqlandi')]
        ]
    )
    await call.message.edit_reply_markup(reply_markup=qabul)
    await call.answer("Zakazni qabul qildingiz!✅", show_alert=True)
    await call.bot.send_message(user_iddd, "<b>Zakaz qabul qilindi✅</b>", parse_mode="HTML",reply_markup=uzz)
    await state.finish()

@dp.callback_query_handler(lambda v:v.data=="yan_z")
async def yan_z(call:types.CallbackQuery,state:FSMContext):
    await state.finish()
    await zakaz(call.message,state)

@dp.callback_query_handler(lambda x:x.data=="rahmat_z")
async def rah_z(call:types.CallbackQuery,state:FSMContext):
    await state.finish()
    await call.answer("Arzimaydi👍",show_alert=True)
    await state.finish()
    await start(call.message,state)


@dp.callback_query_handler(lambda r: r.data == "rad")
async def rad(call: types.CallbackQuery, state: FSMContext):
    qabul = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tasdiqlanmadi❌", callback_data='rad')]
        ]
    )
    await call.message.edit_reply_markup(reply_markup=qabul)
    await call.answer("Zakazni rad etingiz!❌", show_alert=True)
    await call.bot.send_message(user_iddd, "❌<b>Zakaz rad etildi</b>", parse_mode="HTML")
    await state.finish()
download_counts = {}

CHANNEL_ID12="-1002002630375"
# Start komandasini qabul qilish
@dp.message_handler(commands=['start'],state="*")
async def start(msg: Message,state:FSMContext):
    conn = sqlite3.connect('darkmovieuz.db')
   
    
    if " " in msg.text:
        ind = msg.text.index(" ")
        global sd
        sd = (msg.text[ind+1:])

    
        conn = sqlite3.connect('darkmovieuz.db')
        cursor = conn.cursor()

        check_sub_channels = []
        for channel_id in CHANNEL_IDS:
            check_sub_channel = await bot.get_chat_member(chat_id=channel_id, user_id=msg.from_user.id)
            check_sub_channels.append(check_sub_channel)

        # Foydalanuvchi kanalga azo bo'lmagan kanallarni aniqlash
        unsubscribed_channels = [channel_id for i, channel_id in enumerate(CHANNEL_IDS) if check_sub_channels[i].status == "left"]
        if not unsubscribed_channels:
            if sd:
                    conn = sqlite3.connect('darkmovieuz.db')
                    cursor = conn.cursor()
                            
                    cursor.execute("SELECT title, video FROM data WHERE code = ?", (sd,))
                    movie_data = cursor.fetchone()

                    if movie_data:
                        if sd in download_counts:
                            download_counts[sd] += 1
                        else:
                            download_counts[sd] = 1
                        inline = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton(text="Dostlarga yuborish",url=f"https://t.me/share/url/?url=https://t.me/darkmovie_1bot?start={sd}"),
                        InlineKeyboardButton(text="📥Saqlash",callback_data="downn")],
                        [InlineKeyboardButton(text="🛒Saqlanganlar",switch_inline_query_current_chat="",callback_data="kor_kinon")]
                            
                        ],
                        row_width=2 
                    )
                        title, video_file_id = movie_data
                        await bot.send_video(msg.chat.id, video_file_id, caption=f"{title}\n👁:<b>{download_counts[sd]}</b>", reply_markup=inline,parse_mode="HTML")
                        
                        
                    else:
                        await msg.answer("❌Mavjud emas")
                        await state.finish()

                    cursor.close()
                    conn.close()
            else:
                await msg.answer("❌")
                await state.finish()

        else:
        
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            for channel_url in CHANNEL_URLS:
                channel_id = channel_url.split("/")[-1]
                keyboard.add(types.InlineKeyboardButton(text=f"➕Obuna bo'lish", url=channel_url,callback_data="azo"))
                            
            keyboard.add(types.InlineKeyboardButton(text="Azo boldim✅",callback_data="azo_t"))
            cursor.close()
            conn.close()
            await msg.reply(f"⬇️<b>Botdan foydalanish uchun quyidagi kanallarga azo bo'ling:</b>⬇️", reply_markup=keyboard, parse_mode='HTML')
            
            await state.finish()


    else:

        conn = sqlite3.connect('darkmovieuz.db')
        cursor = conn.cursor()
        
        
        user_id = msg.from_user.id

        cursor.execute("SELECT DISTINCT user_id FROM userid")
        existing_user_ids = [row[0] for row in cursor.fetchall()]

        # if user_id not in existing_user_ids:
        #     cursor.execute("SELECT COUNT(DISTINCT user_id) FROM userid")
        #     user_count = cursor.fetchone()[0]

        #     new = f"<b>➕Yangi foydalanuvchi qo'shildi✅</b> \n\n<b>👤Full_Name</b> :<i>{msg.from_user.first_name}</i> \n\n<b>🔢Raqami</b> :<i>{user_count+1}</i>"
        #     await bot.send_message(CHANNEL_ID12, new,parse_mode="HTML")
        
        cursor.execute("INSERT OR IGNORE INTO userid (user_id) VALUES (?)", (user_id,))
        conn.commit()
        

        check_sub_channels = []
        for channel_id in CHANNEL_IDS:
            check_sub_channel = await bot.get_chat_member(chat_id=channel_id, user_id=msg.from_user.id)
            check_sub_channels.append(check_sub_channel)

        # Foydalanuvchi kanalga azo bo'lmagan kanallarni aniqlash
        unsubscribed_channels = [channel_id for i, channel_id in enumerate(CHANNEL_IDS) if check_sub_channels[i].status == "left"]

        if not unsubscribed_channels:
            keyboardd = InlineKeyboardMarkup() # type: ignore
            keyboardd.add(types.InlineKeyboardButton(
                text="📲 Web ilova ochish",
                web_app=types.WebAppInfo(url="https://c8547d7f-6e4e-46fa-90df-0b37cb799d5c-00-4iin8vdwlj1n.pike.replit.dev/")
            ))
            
           
            await msg.answer(f"❗️Assalomu alaykum {msg.from_user.first_name} botimizga xush kelibsiz! \n\n✍️ Kerakli kino kodini yuboring",reply_markup=keyboardd)
            await state.set_state("code")
        else:
        
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            for channel_url in CHANNEL_URLS:
                channel_id = channel_url.split("/")[-1]
                keyboard.add(types.InlineKeyboardButton(text=f"➕Obuna bo'lish ", url=channel_url,callback_data="azo"))
                            
            keyboard.add(types.InlineKeyboardButton(text="Azo boldim✅",callback_data="azo_t"))
            cursor.close()
            conn.close()   
            await msg.reply(f"⬇️<b>Botdan foydalanish uchun quyidagi kanallarga azo bo'ling:</b>⬇️", reply_markup=keyboard, parse_mode='HTML')
            
            await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'downn', state="*")
async def save_movie_callback(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id

    conn = sqlite3.connect('darkmovieuz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_movies WHERE user_id = ? AND movie_code = ?", (user_id, sd))
    existing_entry = cursor.fetchone()
    conn.close()


    if existing_entry:
        await query.answer("❌ Siz avval ushbu kinoni saqlagansiz.",show_alert=True)
    else:
        conn = sqlite3.connect('darkmovieuz.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO saved_movies (user_id, movie_code) VALUES (?, ?)", (user_id, sd))
        conn.commit()
        cursor.close()
        conn.close()

        await query.answer("✅ Ushbu kodli saqlandi!",show_alert=True)

    # Finish the state if needed
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'kor_kinon', state="*")
async def saved_movies_callback(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id

    conn = sqlite3.connect('darkmovieuz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT movie_code FROM saved_movies WHERE user_id = ?", (user_id,))
    saved_movies = cursor.fetchall()
    cursor.close()
    conn.close()

    if saved_movies:
        saved_movie_codes = [str(movie[0]) for movie in saved_movies]

        reply_keyboard = [
            [KeyboardButton(text=code) for code in saved_movie_codes]
        ]

        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        
        await bot.send_message(chat_id=query.from_user.id, text="🎬 Saqlangan kino kodlari:", reply_markup=reply_markup)
    else:
        await query.answer("❌ Siz hali hech qanday kino saqlamagansiz.", show_alert=True)

    await state.finish()

@dp.message_handler(commands=["menyu"],state="*")
async def meny(msg:types.Message,state:FSMContext):
    menu=ReplyKeyboardMarkup(
        keyboard=[
            ["📨Kino yangiliklari","📊Statistika"],
            ["🛒Kino Zakaz","🙋‍♂️Botda muommo bor"],
            ["📑Taklif yoki Reklama berish"]
        ],resize_keyboard=True
    )
    await msg.answer(text="Menyu bo'limiga xush kelibsiz! Agar sizga kodli kino kerakli bo'lsa /start ni bosing",reply_markup=menu)
    await state.set_state("stt")



#Azo bolganligini tekshirish
@dp.callback_query_handler(lambda c: c.data == 'azo_t')
async def callback_subscribe(callback_query: types.CallbackQuery, state: FSMContext):
    
   
    check_sub_channels = []
    for channel_id in CHANNEL_IDS:
        check_sub_channel = await bot.get_chat_member(chat_id=channel_id, user_id=callback_query.from_user.id)
        check_sub_channels.append(check_sub_channel)

    # Foydalanuvchi kanalga azo bo'lmagan kanallarni aniqlash
    unsubscribed_channels = [channel_id for i, channel_id in enumerate(CHANNEL_IDS) if check_sub_channels[i].status == "left"]

    if not unsubscribed_channels:
        await callback_query.message.delete()
        await state.finish()
        await start(callback_query.message,state)
        await state.set_state("code")
    else:
        

        await callback_query.answer(f"❌Botdan foydalanish uchun kanallarga a'zo bolishingiz kerak",show_alert=True )
        await state.finish()




# Define a dictionary to store the number of downloads for each movie code


@dp.message_handler(lambda message: message.text.isdigit(), state="*")
async def check_movie_code(msg: Message, state: FSMContext):
    global download_counts
    conn = sqlite3.connect('darkmovieuz.db')
    cursor = conn.cursor()

    global pyton_code
    pyton_code = msg.text

    check_sub_channels = []
    for channel_id in CHANNEL_IDS:
        check_sub_channel = await bot.get_chat_member(chat_id=channel_id, user_id=msg.from_user.id)
        check_sub_channels.append(check_sub_channel)

    # Foydalanuvchi kanalga azo bo'lmagan kanallarni aniqlash
    unsubscribed_channels = [channel_id for i, channel_id in enumerate(CHANNEL_IDS) if
                             check_sub_channels[i].status == "left"]
    if not unsubscribed_channels:
        if pyton_code.isdigit():
            conn = sqlite3.connect('darkmovieuz.db')
            cursor = conn.cursor()

            cursor.execute("SELECT title, video FROM data WHERE code = ?", (pyton_code,))
            movie_data = cursor.fetchone()

            if movie_data:
                if pyton_code in download_counts:
                    download_counts[pyton_code] += 1
                else:
                    download_counts[pyton_code] = 1

                inline = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="Dostlarga yuborish",
                                              url=f"https://t.me/share/url/?url=https://t.me/darkmovie_1bot?start={pyton_code}"),
                         InlineKeyboardButton(text="📥Saqlash", callback_data="down")],
                        [InlineKeyboardButton(text="🛒Saqlanganlar", switch_inline_query_current_chat="",
                                              callback_data="kor_kino")]
                    ],
                    row_width=2
                )
                title, video_file_id = movie_data
                await bot.send_video(msg.chat.id, video=video_file_id,
                                     caption=f"{title}\n👁:<b>{download_counts[pyton_code]}</b>",
                                     reply_markup=inline, parse_mode="HTML")
            else:
                await msg.answer("❌Bunday kodli kino hozircha mavjud emas")

            cursor.close()
            conn.close()
        else:
            await msg.answer("<b>❗️Iltimos kodni kiriting</b>", parse_mode="HTML")

       
    else:
       
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for channel_url in CHANNEL_URLS:
            channel_id = channel_url.split("/")[-1]
            keyboard.add(types.InlineKeyboardButton(text=f"➕Obuna bo'lish", url=channel_url,callback_data="azo"))
                         
        keyboard.add(types.InlineKeyboardButton(text="Azo boldim✅",callback_data="azo_t"))
        cursor.close()
        conn.close()
        await msg.reply(f"⬇️<b>Botdan foydalanish uchun quyidagi kanallarga azo bo'ling:</b>⬇️", reply_markup=keyboard, parse_mode='HTML')
        
        await state.finish()






#######################################################
@dp.callback_query_handler(lambda c: c.data == 'down', state="*")
async def save_movie_callback(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id

    conn = sqlite3.connect('darkmovieuz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_movies WHERE user_id = ? AND movie_code = ?", (user_id, pyton_code))
    existing_entry = cursor.fetchone()
    conn.close()


    if existing_entry:
        await query.answer("❌ Siz avval ushbu kinoni saqlagansiz.",show_alert=True)
    else:
        conn = sqlite3.connect('darkmovieuz.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO saved_movies (user_id, movie_code) VALUES (?, ?)", (user_id, pyton_code))
        conn.commit()
        cursor.close()
        conn.close()

        await query.answer("✅ Ushbu kodli saqlandi!",show_alert=True)

    # Finish the state if needed
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'kor_kino', state="*")
async def saved_movies_callback(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id

    conn = sqlite3.connect('darkmovieuz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT movie_code FROM saved_movies WHERE user_id = ?", (user_id,))
    saved_movies = cursor.fetchall()
    cursor.close()
    conn.close()

    if saved_movies:
        saved_movie_codes = [str(movie[0]) for movie in saved_movies]

        reply_keyboard = [
            [KeyboardButton(text=code) for code in saved_movie_codes]
        ]

        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        
        await bot.send_message(chat_id=query.from_user.id, text="🎬 Saqlangan kino kodlari:", reply_markup=reply_markup)
    else:
        await query.answer("❌ Siz hali hech qanday kino saqlamagansiz.", show_alert=True)

    await state.finish()



from datetime import datetime as dt

#Statistika
@dp.message_handler(text="📊Statistika", state="*")
async def statistika(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('darkmovieuz.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM userid")
    user_count = cursor.fetchone()[0]

    current_datetime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    
    await message.reply(f"⌚️Statistika vaqt: <b>{current_datetime}</b>\n\n"
                        f"📊Foydalanuvchilar soni: <b>{user_count} ta</b> 👤 mavjud✅\n", parse_mode="HTML")
    
    await state.finish()


@dp.message_handler(text="🙋‍♂️Botda muommo bor",state="*")
async def bot_errors(msg:types.Message,state:FSMContext):
    nazad=ReplyKeyboardMarkup(
        keyboard=[
            ["🔙Ortga"]
        ],resize_keyboard=True
    )
    global user_idddd
    user_idddd = msg.from_user.id
    await msg.answer(
        f"Assalomu alaykum <b>{msg.from_user.first_name}</b>. \n\n<i>Botdagi muommoni yozib qoldiring</i>!✍️",
        parse_mode="HTML",reply_markup=nazad)
    await state.set_state("muommo")

@dp.message_handler(state="muommo",content_types=types.ContentTypes.ANY)
async def muomo(msg:types.Message,state:FSMContext):
    ort=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Bosh sahifa",callback_data="boshiga")]
        ],row_width=2
    )
    user_idd1=msg.from_user.first_name
    ERRORS_BOT='-1002071863566'
    errors=msg.text
    err= InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Bartaraf etish", callback_data='bartaraf'),
             InlineKeyboardButton(text="❌ Rad etish", callback_data='qayt')],
        ],
        row_width=2
    )
    if errors=="🔙Ortga" or errors=="/start":
        await msg.delete()
        await state.finish()
        await start(msg,state)
    else:
        await bot.send_message(text=f"{user_idd1} \nushbu chat egasidan xabar keldi \n\n{errors}", chat_id=ERRORS_BOT, reply_markup=err, parse_mode="Markdown")        
        await state.set_state('bot_error')
        await state.finish()
        await msg.answer("<b>Xabar adminga yuborildi</b>✅\n\n<i>Tez orada sizga admin tomonidan xabar keladi.</i> \t\t\t\t<b>Kuting</b>❗️",
                    parse_mode="HTML",reply_markup=ort)

@dp.callback_query_handler(lambda d:d.data=="boshiga")
async def boshiga(call:types.CallbackQuery,state:FSMContext):
    await call.message.delete()
    await state.finish()
    await start(call.message,state)


@dp.callback_query_handler(lambda z: z.data == "bartaraf",state="*")
async def ad_z(call: types.CallbackQuery, state: FSMContext):
    uzz=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🙋‍♂️Yana muommo bor",callback_data="yan")],
            [InlineKeyboardButton(text="😊Rahmat",callback_data="rahmat")]

        ],row_width=2
    )
    qabul = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Bartaraf qilindi✅", callback_data='bartaraf')]
        ]
    )
    await call.message.edit_reply_markup(reply_markup=qabul)
    await call.answer("Muommo bartaraf qilindi!✅", show_alert=True)
    await call.bot.send_message(user_idddd, "<b>Muommo bartaraf qilindi✅</b>", parse_mode="HTML",reply_markup=uzz)
    await state.finish()

@dp.callback_query_handler(lambda v:v.data=="yan",state="*")
async def yan(call:types.CallbackQuery,state:FSMContext):
    await state.finish()
    await bot_errors(call.message,state)

@dp.callback_query_handler(lambda x:x.data=="rahmat",state="*")
async def rah(call:types.CallbackQuery,state:FSMContext):
    await call.message.delete()
    await state.finish()
    await call.answer("Arzimaydi👍",show_alert=True)
    await state.finish()
    await start(call.message,state)


@dp.callback_query_handler(lambda r: r.data == "qayt",state="*")
async def rad(call: types.CallbackQuery, state: FSMContext):
    qabul = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tasdiqlanmadi❌", callback_data='qayt')]
        ]
    )
    await call.message.edit_reply_markup(reply_markup=qabul)
    await call.answer("Muommo bartaraf qilinmadi!❌", show_alert=True)
    await call.bot.send_message(user_iddd, "❌<b>Xabaringiz rad etildi</b>", parse_mode="HTML")
    await state.finish()




#Kanalga post joylash


#Taklif va reklama
@dp.message_handler(text="📑Taklif yoki Reklama berish",state="*")
async def taklifandrek(msg:Message,state:FSMContext):
    admin=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📲Admin bilan bog'lanish",url="https://t.me/python_chi")],
            [InlineKeyboardButton(text="❌Tugatish",callback_data="st")]
        ],row_width=2
    )
    await msg.answer("Taklif va Reklama uchun <b>📲Admin bilan bog'lanish</b> tugmasini bosing⤵️ \n\n❗️<b>Eslatma</b>: \n<i>Faqat taklif va reklama uchun yozing <b>yo'qsa, bloklanasiz!</b></i>",reply_markup=admin,parse_mode="HTML")
    await state.set_state("st")
    await state.finish()


@dp.callback_query_handler(lambda s:s.data=="st")
async def st(call:types.CallbackQuery,state:FSMContext):
    await call.message.delete()
    await state.finish()
    await start(call.message,state)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)


