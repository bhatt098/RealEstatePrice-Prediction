from housing.pipeline.pipeline import*
import re



def main():
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    print(re.match(regex, "http://www.example.com") is not None) # True
    print(re.match(regex, "example.com") is not None)  
    pipeline=Pipeline()
    pipeline.run_pipeline()

if __name__=="__main__":
    main()