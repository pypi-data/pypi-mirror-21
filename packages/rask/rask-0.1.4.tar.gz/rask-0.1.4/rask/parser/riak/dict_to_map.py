from base64 import b64encode
from rask.base import Base
from rask.options import options

__all__ = ['DictToMap']

class DictToMap(Base):
    @property
    def recipes(self):
        try:
            assert self.__recipes
        except (AssertionError,AttributeError):
            self.__recipes = {
                'bool':self.__recipe_bool,
                'float':self.__recipe_str,
                'int':self.__recipe_str,
                'set':self.__recipe_set,
                'set+':self.__recipe_set_add,
                'set-':self.__recipe_set_discard,
                'str':self.__recipe_str,
                'unicode':self.__recipe_unicode,
                'utcode':self.__recipe_utcode
            }
        except:
            raise
        return self.__recipes

    def __recipe_bool(self,key,data,record,schema,future):
        try:
            assert data[key]
        except AssertionError:
            record.flags[key].disable()
        except:
            raise
        else:
            record.flags[key].enable()
        return future.set_result(record)

    def __recipe_set(self,key,data,record,schema,future):
        for v in data[key]:
            try:
                assert 'set%s' % v[0] in self.recipes
            except (AssertionError,IndexError):
                pass
            except:
                raise
            else:
                record = self.recipes['set%s' % v[0]](key,v,record)
        return future.set_result(record)

    def __recipe_set_add(self,key,value,record):
        record.sets[key].add(str(value[1:]))
        return record

    def __recipe_set_discard(self,key,value,record):
        record.sets[key].discard(str(value[1:]))
        return record

    def __recipe_str(self,key,data,record,schema,future):
        record.registers[key].assign(str(data[key]))
        return future.set_result(record)

    def __recipe_unicode(self,key,data,record,schema,future):
        record.registers[key].assign(b64encode(data[key]))
        return future.set_result(record)

    def __recipe_utcode(self,key,data,record,schema,future):
        def on_encode(_):
            record.registers[key].assign(_.result())
            return future.set_result(record)
        
        return options.utcode.encode(
            data[key],
            future=self.ioengine.future(on_encode)
        )

    def consume(self,data,record,schema,i,future):
        try:
            key = i.next()
            assert schema[key]['recipe'] in self.recipes
        except (AssertionError,KeyError):
            pass
        except StopIteration:
            future.set_result(record)
            return True
        except:
            raise
        else:
            def on_recipe(_):
                return self.ioengine.loop.add_callback(
                    self.consume,
                    data=data,
                    record=_.result(),
                    schema=schema,
                    i=i,
                    future=future
                )
            
            self.ioengine.loop.add_callback(
                self.recipes[schema[key]['recipe']],
                key=key,
                data=data,
                record=record,
                schema=schema,
                future=self.ioengine.future(on_recipe)
            )

        return None
    
    def process(self,data,record,schema,future):
        return self.ioengine.loop.add_callback(
            self.consume,
            data=data,
            record=record,
            schema=schema,
            i=iter(data),
            future=future
        )
