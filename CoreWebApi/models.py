from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship, backref
from CoreWebApi.database import Base

class Products(Base):
	__tablename__ = 'products'
	upc = Column(String(13), ForeignKey('productUser.upc'), ForeignKey('prodExtra.upc'), primary_key=True)
	description = Column(String(255))
	normal_price = Column(Numeric(10,2))
	special_price = Column(Numeric(10,2))
	discounttype = Column(Integer)
	scale = Column(Integer)

	productUser = relationship("ProductUser", backref=backref("products", uselist=False))
	prodExtra = relationship("ProdExtra", backref=backref("products", uselist=False))

	def __repr__(self):
		return '<Product %r>' % (self.upc)

	def serialize(self):
		repr = {}
		repr['upc'] = self.upc
		repr['price'] = round(self.normal_price,2)
		if (self.discounttype == 1):
			repr['salePrice'] = round(self.special_price,2)
		elif(self.discounttype == 2):
			repr['memPrice'] = round(self.special_price,2)
		if self.scale == 1:
			repr['per_lb'] = True

		repr['description'] = self.description
		if self.productUser != None and self.productUser.description != "":
			repr['description'] = self.productUser.description
		repr['brand'] = 'n/a'
		if self.productUser != None and self.productUser.brand != "":
			repr['brand'] = self.productUser.brand
		elif self.prodExtra != None and self.prodExtra.manufacturer != "":
			repr['brand'] = self.prodExtra.manufacturer
		return repr

class ProdExtra(Base):
	__tablename__ = 'prodExtra'
	upc = Column(String(13), primary_key=True)
	manufacturer = Column(String)

class ProductUser(Base):
	__tablename__ = 'productUser'
	upc = Column(String(13), primary_key=True)
	description = Column(String(255))
	brand = Column(String(255))
	sizing = Column(String(255))
	photo = Column(String(255))
	long_text = Column(Text)
	enableOnline = Column(Integer)

	def __repr__(self):
		return '<ProductUser %r>' % (self.upc)

	def serialize(self):
		return {
			'upc' : self.upc,
			'description' : self.description,
			'brand' : self.brand,
			'size' : self.sizing
		}
