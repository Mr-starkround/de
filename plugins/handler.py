import re

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from plugins import Database, Helper
from plugins.command import *
from bot import Bot


@Bot.on_message()
async def on_message(client: Client, msg: Message):
    if msg.chat.type == enums.ChatType.PRIVATE:
        if msg.from_user is None:
            return
        else:
            uid = msg.from_user.id
        helper = Helper(client, msg)
        database = Database(uid)

        # cek apakah user sudah bergabung digrup chat
        if not await helper.cek_langganan_channel(uid):
            return await helper.pesan_langganan()  # jika belum akan menampilkan pesan bergabung

        if not await database.cek_user_didatabase():  # cek apakah user sudah ditambahkan didatabase
            await helper.daftar_pelanggan()  # jika belum akan ditambahkan data user ke database
            await helper.send_to_channel_log(type="log_daftar")

        # Pesan jika bot sedang dalam kondisi tidak aktif
        if not database.get_data_bot(client.id_bot).bot_status:
            status = [
                'member', 'banned', 'talent', 'daddy sugar', 'moans girl',
                'moans boy', 'girlfriend rent', 'boyfriend rent'
            ]
            member = database.get_data_pelanggan()
            if member.status in status:
                return await client.send_message(uid, "<i>Saat ini bot sedang dinonaktifkan</i>", enums.ParseMode.HTML)

        command = msg.text or msg.caption
        if command is None:
            await gagal_kirim_handler(client, msg)

        else:
            if command == '/start':  # menampilkan perintah start
                return await start_handler(client, msg)

            elif command == '/help':
                return await help_handler(client, msg)

            elif command == '/status':  # menampilkan perintah status
                return await status_handler(client, msg)

            elif command == '/list_admin':  # menampilkan perintah list admin
                return await list_admin_handler(helper, client.id_bot)

            elif command == '/list_ban':  # menampilkan perintah list banned
                return await list_ban_handler(helper, client.id_bot)

            elif command == '/talent':
                return await talent_handler(client, msg)

            elif command == '/daddysugar':
                return await daddy_sugar_handler(client, msg)

            elif command == '/moansgirl':
                return await moans_girl_handler(client, msg)

            elif command == '/moansboy':
                return await moans_boy_handler(client, msg)

            elif command == '/gfrent':
                return await gf_rent_handler(client, msg)

            elif command == '/bfrent':
                return await bf_rent_handler(client, msg)

            elif command == '/stats':  # menampilkan perintah statistik
                if uid == config.id_admin:
                    return await statistik_handler(helper, client.id_bot)

            elif command == '/broadcast':
                if uid == config.id_admin:
                    return await broadcast_handler(client, msg)

            elif command in ['/settings', '/setting']:  # menampilkan perintah settings
                member = database.get_data_pelanggan()
                if member.status in ['admin', 'owner']:
                    return await setting_handler(client, msg)

            elif re.search(r"^[\/]rate", command):
                return await rate_talent_handler(client, msg)

            elif re.search(r"^[\/]tf_coin", command):
                return await transfer_coin_handler(client, msg)

            elif re.search(r"^[\/]bot", command):  # menonaktifkan dan mengaktifkan bot
                if uid == config.id_admin:
                    return await bot_handler(client, msg)

            elif re.search(r"^[\/]admin", command):  # menambahkan admin baru
                if uid == config.id_admin:
                    return await tambah_admin_handler(client, msg)

            elif re.search(r"^[\/]unadmin", command):
                if uid == config.id_admin:
                    return await hapus_admin_handler(client, msg)

            elif re.search(r"^[\/]addtalent", command):  # menambahkan talent baru
                if uid == config.id_admin:
                    return await tambah_talent_handler(client, msg)

            elif re.search(r"^[\/]addsugar", command):  # menambahkan daddy sugar baru
                if uid == config.id_admin:
                    return await tambah_sugar_daddy_handler(client, msg)

            elif re.search(r"^[\/]addgirl", command):  # menambahkan moans girl baru
                if uid == config.id_admin:
                    return await tambah_moans_girl_handler(client, msg)

            elif re.search(r"^[\/]addboy", command):  # menambahkan moans boy baru
                if uid == config.id_admin:
                    return await tambah_moans_boy_handler(client, msg)

            elif re.search(r"^[\/]addgf", command):  # menambahkan gf rent baru
                if uid == config.id_admin:
                    return await tambah_gf_rent_handler(client, msg)

            elif re.search(r"^[\/]addbf", command):  # menambahkan bf rent baru
                if uid == config.id_admin:
                    return await tambah_bf_rent_handler(client, msg)

            elif re.search(r"^[\/]hapus", command):  # menambahkan mengapus talent
                if uid == config.id_admin:
                    return await hapus_talent_handler(client, msg)

            elif re.search(r"^[\/]ban", command):  # membanned user
                member = database.get_data_pelanggan()
                if member.status in ['admin', 'owner']:
                    return await ban_handler(client, msg)

            elif re.search(r"^[\/]unban", command):  # membuka kembali banned kepada user
                member = database.get_data_pelanggan()
                if member.status in ['admin', 'owner']:
                    return await unban_handler(client, msg)

            # handler untuk perintah /cek
            elif re.search(r"^[\/]cek", command):
                return await cek_handler(client, msg)

            if x := re.search(fr"(?:^|\s)({config.hastag})", command.lower()):
                key = x[1]
                hastag = config.hastag.split('|')
                member = database.get_data_pelanggan()
                if member.status == 'banned':
                    return await msg.reply(f'Kamu telah <b>di banned</b>\n\n<u>Alasan:</u> {database.get_data_bot(client.id_bot).ban[str(uid)]}\nsilahkan kontak @OwnNeko untuk unbanned', True, enums.ParseMode.HTML)
                if key in [hastag[0], hastag[1]]:
                    return (
                        await msg.reply(
                            '🙅🏻‍♀️  post gagal terkirim, <b>mengirim pesan wajib lebih dari 3 kata.</b>',
                            True,
                            enums.ParseMode.HTML,
                        )
                        if key == command.lower()
                        or len(command.split(' ')) < 3     
                         else await send_menfess_handler(
                            client, msg, hastag
                        )
                    )
                elif key in hastag:
                    if key == command.lower() or len(command.split(' ')) < 3:
                        return await msg.reply('🙅🏻‍♀️  post gagal terkirim, <b>mengirim pesan wajib lebih dari 3 kata.</b>', True, enums.ParseMode.HTML)
                    else:
                        return await send_menfess_handler(client, msg)
                else:
                    await send_menfess(client, msg)
            else:
                await gagal_kirim_handler(client, msg) 
    elif msg.chat.type == enums.ChatType.SUPERGROUP:
        command = msg.text or msg.caption
        if msg.from_user is None:
            if msg.sender_chat.id != config.channel_1:
                return

            if x := re.search(fr"(?:^|\s)({config.hastag})", command.lower()):
                hastag = config.hastag.split('|')
                if x[1] in [hastag[0], hastag[1]]:
                    try:
                        await client.delete_messages(msg.chat.id, msg.id)
                    except:
                        pass
        else:
            uid = msg.from_user.id
        if command != None:
            return


@Bot.on_callback_query()
async def on_callback_query(client: Client, query: CallbackQuery):
    if query.data == 'photo':
        await photo_handler_inline(client, query)
    elif query.data == 'video':
        await video_handler_inline(client, query)
    elif query.data == 'voice':
        await voice_handler_inline(client, query)
    elif query.data == 'status_bot':
        if query.message.chat.id == config.id_admin:
            await status_handler_inline(client, query)
        else:
            await query.answer('Ditolak, kamu tidak ada akses', True)
    elif query.data == 'ya_confirm':
        await broadcast_ya(client, query)
    elif query.data == 'tidak_confirm':
        await close_cbb(client, query)
