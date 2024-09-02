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
    item_use:bool=1#各時間帯のアイテム使用権（Ture：未使用、False：使用済み）
    not_attacked:bool=False#襲撃されない（True：されない、False：される）
    unidentifiable:bool=False#判別不可（True：されない、False：される）
    escorted:bool=False#護衛されているか（True：されている、False：されていない）
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