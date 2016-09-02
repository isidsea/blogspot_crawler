from lib.data.factory   		    import DataFactory
from lib.converter_engine.interface import ConverterInterface

if __name__ == "__main__":
	print("[convert][debug] Converting...")
	ConverterInterface.multiple_convert_and_save(data=DataFactory.get_data(DataFactory.POST))
	print("[convert][debug] Converted!")