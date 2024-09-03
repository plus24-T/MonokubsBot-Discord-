import discord

import dataclasses
#参加キャラのデータを格納するクラス
@dataclasses.dataclass#役職のデータを格納するクラス
class CharaRole:
    id:int=0#役職に対応した数字、下記変換辞書参照
    name:str="未定"#役職の名前
@dataclasses.dataclass
class CharaData:
    role:CharaRole= dataclasses.field(default_factory=CharaRole)#役職idとname
    chara_ability:str=""#キャラ名（石田のコピー時ここを変えて参照する）
    ability_use:bool=True#キャラ能力使用状況（True：未使用、False：使用済み）
    num_of_items:int=0#所持アイテム数
    item_1_id:int=0#所持アイテム一つ目 intじゃ情報足りないので辞書咬ませてデータクラスとかになりそう
    item_2_id:int=0#所持アイテム二つ目
    votes:int=1#所持票数（投票無効時0にする）
    item_use:bool=True#各時間帯のアイテム使用権（Ture：未使用、False：使用済み）
    not_attacked:bool=False#襲撃されない（True：されない、False：される）
    unidentifiable:bool=False#判別不可（True：されない、False：される）
    escorted:bool=False#襲撃無効が付与されているか（True：されている、False：されていない）
    position=int#席の位置、生存人数の剰余で隣り合っているか判定する

CC_02 = CharaData()
CC_03 = CharaData()
CC_04 = CharaData()
CC_05 = CharaData()
CC_06 = CharaData()
CC_07 = CharaData()
CC_08 = CharaData()
CC_09 = CharaData()
CC_10 = CharaData()
CC_11 = CharaData()
CC_12 = CharaData()
CC_13 = CharaData()
CC_14 = CharaData()
CC_15 = CharaData()
CC_16 = CharaData()
CC_17 = CharaData()
CC_18 = CharaData()
CC_19 = CharaData()
CC_20 = CharaData()
CC_21 = CharaData()
CC_22 = CharaData()
CC_23 = CharaData()
CC_24 = CharaData()
CC_25 = CharaData()
CC_26 = CharaData()
CC_27 = CharaData()
CC_28 = CharaData()
CC_29 = CharaData()
CC_30 = CharaData()
CC_31 = CharaData()
CC_32 = CharaData()
CC_33 = CharaData()
CC_34 = CharaData()
CC_35 = CharaData()
MCC_01 = CharaData()
MCC_02 = CharaData()
MCC_03 = CharaData()
MCC_04 = CharaData()
MCC_05 = CharaData()
MCC_06 = CharaData()
MCC_07 = CharaData()
MCC_08 = CharaData()
MCC_09 = CharaData()
MCC_10 = CharaData()

#キャラ名からデータクラスへの変換辞書
nick_to_data={
    "苗木誠":CC_02,
    "舞園さやか":CC_03,
    "桑田怜恩":CC_04,
    "霧切響子":CC_05,
    "十神白夜":CC_06,
    "山田一二三":CC_07,
    "大和田紋土":CC_08,
    "腐川冬子":CC_09,
    "セレスティアルーデンベルク":CC_10,
    "朝日奈葵":CC_11,
    "石丸清多夏":CC_12,
    "大神さくら":CC_13,
    "葉隠康比呂":CC_14,
    "江ノ島盾子":CC_15,
    "不二咲千尋":CC_16,
    "ジェノサイダー翔":CC_17,
    "戦刃むくろ":CC_18,
    "江ノ島盾子：絶望":CC_19,
    "霧切響子：カップ麵":MCC_01,
    "石丸清多夏：石田":MCC_08,
    "江ノ島盾子：王冠":MCC_09,
    "日向創":CC_20,
    "狛枝凪斗":CC_21,
    "田中眼蛇夢":CC_22,
    "左右田和一":CC_23,
    "十神白夜：ジャバウォック島のすがた":CC_24,
    "花村輝々":CC_25,
    "弐大猫丸":CC_26,
    "九頭龍冬彦":CC_27,
    "終里赤音":CC_28,
    "七海千秋":CC_29,
    "ソニアネヴァーマインド":CC_30,
    "西園寺日寄子":CC_31,
    "小泉真昼":CC_32,
    "罪木蜜柑":CC_33,
    "澪田唯吹":CC_34,
    "辺古山ペコ":CC_35,
    "狛枝凪斗：絶望":MCC_02,
    "左右田和一：楳図かずお画風":MCC_03,
    "十神白夜：腕組み":MCC_05,
    "花村輝々：鼻血":MCC_07,
    "弐大猫丸：メカ":MCC_10,
    "七海千秋：唾吐き":MCC_06,
    "西園寺日寄子：てへぺろ":MCC_04
}    
#各役職がどのキャラクターかを格納する変数　キャスト（配役）リスト
@dataclasses.dataclass
class CastLists:
    siro:list[discord.Member]=dataclasses.field(default_factory=list)
    alterego:list[discord.Member]=dataclasses.field(default_factory=list)
    miraikikan:list[discord.Member]=dataclasses.field(default_factory=list)
    tyozetsubo:list[discord.Member]=dataclasses.field(default_factory=list)
    zetsubobyo:list[discord.Member]=dataclasses.field(default_factory=list)
    monomi:list[discord.Member]=dataclasses.field(default_factory=list)
    kuro:list[discord.Member]=dataclasses.field(default_factory=list)
    uragiri:list[discord.Member]=dataclasses.field(default_factory=list)
    zako:list[discord.Member]=dataclasses.field(default_factory=list)
    zantou:list[discord.Member]=dataclasses.field(default_factory=list)

Cast=CastLists()
#ゲーム進行にまつわるint変数
player:int = 0 #（ゲームに参加しない場合のGMを除いた）プレイヤー数
kill:int = 0 #　殺害数（ゲーム終了トリガーとして参照
day:int = 0 #　何日目か（能力使用の条件として参照、司会進行メッセージで参照
#出揃い待ち用のint変数
role_registered:int = 0 #役職登録済みプレイヤー数（全員登録終わってからにクロ裏切者通知する用
remaining_processes:int=0#夜時間に処理する対象選択や判別の数、全て処理してから相互作用の確認後、朝へ