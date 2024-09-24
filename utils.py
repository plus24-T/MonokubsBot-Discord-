import discord
from discord.ext import commands

import gv
import views

# あちこちで使う類似のメソッド（関数）を記述する

# キャラ選択後の共通処理
async def on_chara_selected(interaction: discord.Interaction, select: discord.ui.Select, bot : commands.bot):
    user_nickname = select.values[0]
    await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name=user_nickname))
    gv.get_chara_data(user_nickname).chara_ability=user_nickname
    await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name="生存"))
    try:
        await interaction.user.edit(nick=user_nickname)
    except Exception as e:
        print(e)
    await interaction.response.send_message(
        f"よくきたな{user_nickname}\nさっさと"
        f"{discord.utils.get(interaction.guild.channels,name=user_nickname).mention}"
        "に移動してロールを登録してくるんだな",
        ephemeral=True
        )
    await discord.utils.get(interaction.guild.channels,name=user_nickname).send(
        "ロール、ノ登録ヲ、オ願イスルヨ",
        view=views.RoleSleMenu(bot)
    )

# 希望・絶望サイド判定（占い）  絶望サイド：True  希望サイド：False
def check_despair(interaction: discord.Interaction, target_chara_name : str) -> bool:
    # 希望サイド判定を行う閾値
    any_member_died : bool = len(discord.utils.get(interaction.guild.roles,name="死亡").members) > 0
    despair_threshold = gv.CharaRole.get_despair_threshold(any_member_died)
    target_role = gv.get_chara_data(target_chara_name).role
    
    if target_role.value <= despair_threshold.value:
        return False
    else:
        if target_role != gv.CharaRole.KURO:
            return True
        else:
            if len(gv.chara_role_list.zantou) == 0:
                return True
            else:
                if gv.chara_role_list.zantou[0] in discord.utils.get(interaction.guild.roles,name="死亡").members:
                    return True
                else:
                    return False