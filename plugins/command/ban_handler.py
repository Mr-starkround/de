import config
import re

from pyrogram import Client, enums, types
from plugins import Database


async def ban_handler(client: Client, msg: types.Message):
    if re.search(r"^[\/]ban(\s|\n)*$", msg.text):
        return await msg.reply_text(
            text="<b>Cara penggunaan ban user</b>\n\n<code>/ban id_user alasan ban</code>\n<code>/ban id_user</code>\n\nContoh :\n<code>/ban 121212021</code>\n<code>/ban 12121 share porn</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    if not (y := re.search(r"^[\/]ban(\s|\n)*(\d+)", msg.text)):
        return await msg.reply_text(
            text="<b>Cara penggunaan ban user</b>\n\n<code>/ban id_user alasan ban</code>\n<code>/ban id_user</code>\n\nContoh :\n<code>/ban 121212021</code>\n<code>/ban 12121 share porn</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    target = y[2]
    db = Database(int(target))
    if not await db.cek_user_didatabase():
        return await msg.reply_text(
            text=f"<i>{await get_user_mention(target, client)}</i> tidak terdaftar didatabase",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    status = [
        'admin', 'owner', 'talent', 'daddy sugar', 'moans girl',
        'moans boy', 'girlfriend rent', 'boyfriend rent'
    ]
    member = db.get_data_pelanggan()
    if member.status == 'admin' in status:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, {await get_user_mention(target, client)} adalah seorang {member.status.upper()} tidak dapat dibanned</i>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    update = 'Alasan berhasil diupdate' if member.status == 'banned' else ''
    text_split = msg.text.split(None, 2)
    alasan = "-" if len(text_split) <= 2 else text_split[2]
    await db.banned_user(int(target), client.id_bot, alasan)

    admin_mention = await get_user_mention(config.id_admin, client)  # Assign admin_mention before using it
    # Send notification to channel_1
    notification_text = f"User <a href='tg://user?id={str(target)}'> {await get_user_mention(target, client)} </a> dengan Id: <code>{target}</code> sudah di banned. karena: {alasan}\n\noleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>{admin_mention}</a>"
    await client.send_message(config.channel_1, notification_text)

    return await msg.reply_text(
        text=f"<a href='tg://user?id={str(target)}'> {await get_user_mention(target, client)} </a> <i>berhasil dibanned</i>\n└Dibanned oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>{admin_mention}</a>\n\nAlasan: {str(alasan)}\n\n{update}",
        quote=True,
        parse_mode=enums.ParseMode.HTML
    )


async def unban_handler(client: Client, msg: types.Message):
    if re.search(r"^[\/]unban(\s|\n)*$", msg.text):
        return await msg.reply_text(
            text="<b>Cara penggunaan unban user</b>\n<code>/unban id_user alasan unbanned</code>\n\nContoh :\n<code>/unban 121212021</code>\n<code>/unban 12121 sudah selesai</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    if not (x := re.search(r"^[\/]unban(\s|\n)*(\d+)", msg.text)):
        return await msg.reply_text(
            text="<b>Cara penggunaan unban user</b>\n<code>/unban id_user alasan unbanned</code>\n\nContoh :\n<code>/unban 121212021</code>\n<code>/unban 12121 sudah selesai</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    target = x[2]
    db = Database(int(target))
    if not await db.cek_user_didatabase():
        return await msg.reply_text(
            text=f"<i>{await get_user_mention(target, client)}</i> tidak terdaftar didatabase",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    if target in db.get_data_bot(client.id_bot).ban:
        await db.unban_user(int(target), client.id_bot)

        admin_mention = await get_user_mention(config.id_admin, client)  # Assign admin_mention before using it
        # Send notification to channel_1
        notification_text = f"User <a href='tg://user?id={str(target)}'> {await get_user_mention(target, client)} </a> dengan Id:<code> {target}</code> sudah di unban. \n\noleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>{admin_mention}</a>"
        await client.send_message(config.channel_1, notification_text)

        return await msg.reply_text(
            text=f"<a href='tg://user?id={str(target)}'> {await get_user_mention(target, client)} </a> <i>berhasil diunbanned</i>\n└Diunbanned oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>{admin_mention}</a>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    else:
        return await msg.reply_text(
            text=f"<i>{await get_user_mention(target, client)}</i> sedang tidak dalam kondisi banned",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )


async def cek_handler(client: Client, msg: types.Message):
    if not (z := re.search(r"^[\/]cek(\s|\n)*(\d+)", msg.text)):
        return await msg.reply_text(
            text="<b>Cara penggunaan cek user</b>\n<code>/cek id_user</code>\n\nContoh :\n<code>/cek 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    target = z[2]
    db = Database(int(target))
    if not await db.cek_user_didatabase():
        return await msg.reply_text(
            text=f"<i>{await get_user_mention(target, client)}</i> tidak terdaftar didatabase",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    user_data = db.get_data_pelanggan()
    ban_reason = db.get_data_bot(client.id_bot).ban.get(target, "Tidak ada alasan yang tersedia.")
    
    # Check user role and allow only owner, admin, talent, and member to see data
    allowed_roles = ['owner', 'admin', 'talent', 'member']
    if user_data.status not in allowed_roles:
        return await msg.reply_text(
            text="<i>Anda tidak memiliki izin untuk melihat data pengguna ini.</i>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    
    return await msg.reply_text(
        text=f"Data pengguna:\n\nID Pengguna: {user_data.id}\nUsername: {user_data.username}\nNama: {user_data.nama}\nStatus: {user_data.status}\nMenfess: {user_data.menfess}\nAlasan Banned: {ban_reason}",
        quote=True,
        parse_mode=enums.ParseMode.HTML
    )



async def get_user_mention(user_id: str, client: Client):
    user_info = await client.get_users(int(user_id))
    mention_name = user_info.first_name if not user_info.last_name else f"{user_info.first_name} {user_info.last_name}"
    return mention_name


async def get_mention_name(user_id: str, client: Client):
    user_info = await client.get_users(int(user_id))
    mention_name = user_info.first_name if not user_info.last_name else f"{user_info.first_name} {user_info.last_name}"
    return mention_name
