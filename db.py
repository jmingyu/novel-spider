from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class main(Base):
    # 表的名字:
    __tablename__ = 'main'

    # 表的结构:
    id = Column(String(11), primary_key=True)
    title = Column(String(128))
    detail = Column(String())
    mainurl = Column(String(512))
    cat = Column(String(128))
    author = Column(String(64))
    no = Column(String(512))

def connect(params):
    # 初始化数据库连接:
    print(params[0])
    engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/novel')
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)


    # 创建session对象:
    session = DBSession()
    # 创建新User对象:
    new_main = main(id=params[0],title=params[1],detail=params[2],mainurl=params[3],cat=params[4],author=params[5],no=params[6])
    # new_main = main(params)
    # 添加到session:
    session.add(new_main)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()
    print('入库成功')