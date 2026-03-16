import traceback,time
class TestRunner:
    def __init__(self): self.tests=[]; self.results=[]
    def test(self,name):
        def decorator(fn): self.tests.append((name,fn)); return fn
        return decorator
    def run(self):
        passed=failed=errors=0
        for name,fn in self.tests:
            try:
                fn()
                self.results.append(('PASS',name,None)); passed+=1
                print(f"  ✅ {name}")
            except AssertionError as e:
                self.results.append(('FAIL',name,str(e))); failed+=1
                print(f"  ❌ {name}: {e}")
            except Exception as e:
                self.results.append(('ERROR',name,str(e))); errors+=1
                print(f"  💥 {name}: {e}")
        total=passed+failed+errors
        print(f"\n{passed}/{total} passed, {failed} failed, {errors} errors")
        return failed+errors==0
def assert_eq(a,b,msg=None):
    if a!=b: raise AssertionError(msg or f"Expected {b}, got {a}")
def assert_raises(exc_type,fn):
    try: fn(); raise AssertionError(f"Expected {exc_type.__name__}")
    except exc_type: pass
if __name__=="__main__":
    runner=TestRunner()
    @runner.test("addition")
    def _(): assert_eq(1+1,2)
    @runner.test("string")
    def _(): assert_eq("hello".upper(),"HELLO")
    @runner.test("raises")
    def _(): assert_raises(ZeroDivisionError,lambda:1/0)
    @runner.test("failing")
    def _(): assert_eq(1,2,"one != two")
    success=runner.run()
    assert not success  # one test fails
    assert sum(1 for r in runner.results if r[0]=='PASS')==3
    print("\nAll tests passed!")
