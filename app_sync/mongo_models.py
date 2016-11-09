from mongoengine import Document, StringField, IntField, ListField, DateTimeField, ObjectIdField, FloatField


class Blocks(Document):
    totalDifficulty = IntField(required=True)
    mixHash = StringField(required=False)
    miner = StringField(required=True)
    gasUsed = IntField(required=True)
    logsBloom = StringField(required=True)
    sha3Uncles = StringField(required=True)
    uncles = ListField(null=True)
    extraData = StringField(required=True)
    difficulty = IntField(required=True)
    size = IntField(required=True)
    number = IntField(required=True, unique=True)
    transactionsRoot = StringField(required=True)
    timestamp = IntField(required=True)
    receiptRoot = StringField(required=False)
    receiptsRoot = StringField(required=False)
    parentHash = StringField(required=True)
    transactions = ListField(null=True)
    nonce = StringField(required=True)
    hash = StringField(required=True)
    stateRoot = StringField(required=True)
    gasLimit = IntField(required=True)
    created = DateTimeField(required=True)

    meta = {
        'indexes': [
            'number',
            'created',
        ]
    }


class Transactions(Document):
    fromAddress = StringField(required=True)
    toAddress = StringField(required=True)
    input = StringField(required=True)
    blockHash = StringField(required=True)
    hash = StringField(required=True)
    nonce = IntField(required=True)
    value = FloatField(required=True)
    transactionIndex = IntField(required=True)
    gas = IntField(required=True)
    gasPrice = IntField(required=True)
    blockNumber = IntField(required=True)
    block = ObjectIdField(required=True)

    meta = {
        'indexes': [
            'fromAddress',
            'toAddress',
            'hash',
            'block',
            'value',
        ]
    }
