import re


# PII = Personally Identifiable Information
# Create a new Pii class based on str
class Pii(str):
    # For help with regex see
    # https://regex101.com
    # https://www.w3schools.com/python/python_regex.asp

    def has_us_phone(self, anonymize=False):
        newstr, count1 = re.subn(r'\d{9}', '[us phone]', self)

        newstr, count2 = re.subn(r'\d{3}[-.]\d{3}[-.]\d{4}', '[us phone]', newstr)

        if anonymize:
            return newstr
        else:
            return bool(count2 + count1)

    def has_email(self, anonymize = False):
       # em = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9]{2,}\b', self)
        #if em:
       #     return True
        #return None
        newstr, count1 = re.subn(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.]{2,}\b', '[email]', self)

        print(newstr)
        print (bool(count1))
        if anonymize:
            return newstr
        else:
           return bool(count1)

    def has_ipv4(self, anonymize = False):
        match = re.sub('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}','[ipv4 address]', self)
        if anonymize:
            return match
        else:
            return True if match != self else None

    def has_ipv6(self, anonymize=False):
        newstr, count1 = re.subn(r'((\b[0-9a-fA-F]{0,4}\b)?:(\b[0-9a-fA-F]{0,4}\b)?:'
                                 r'(\b[0-9a-fA-F]{0,4}\b)?:(\b[0-9a-fA-F]{0,4}\b)?:'
                                 r'(\b[0-9a-fA-F]{0,4}\b)?:(\b[0-9a-fA-F]{0,4}\b)?:'
                                 r'(\b[0-9a-fA-F]{0,4}\b)?:(\b[0-9a-fA-F]{0,4}\b)?$)', '[ipv6]', self)

        if anonymize:
            return newstr
        else:
            return bool(count1)

    def has_name(self, anonymize=False):
        newstr, count1 = re.subn(r'(?<!\d )[A-Z][a-z]+ [A-Z][a-z]+', '[name]', self)
        print(newstr)
        print(count1)
        if anonymize:
            return newstr
        else:
            return bool(count1)

    def has_street_address(self, anonymize=False):
        newstr, count1 = re.subn(r'(?<=\s)\d{0,4}\s[A-Z][a-zA-Z]{2,30}\s\b(Ave|St|Blvd|Rd)\b', '[street address]', self)
        print(newstr)
        print(bool(count1))

        if anonymize:
            return newstr
        else:
            return bool(count1)

    def has_credit_card(self, anonymize = False):
        newstr, count1 = re.subn(r'\d{4}-\d{4}-\d{4}-\d{4}', '[credit card]', self)

        if anonymize:
            # Since str is immutable it's better to stay with the spec and return a new
            # string rather than modifying self
            return newstr
        else:
            # Keep the original requirement in place by returning True or False if
            # a us phone number was present or not.
            return bool(count1)

    def has_at_handle(self, anonymize = False):
        #hand = re.search(r'^@[A-Za-z0-9._-]{1,}', self)
        #hand = re.search(r'^[\w@](?!.*?\.{2})[\w.]{1,28}[\w]$', self)

        #r'^[\w@](?!.*?\.{2})[\w.]{1,28}[\w]$'

        #hand = re.sub(r'[\@][A-z0-9][A-z0-9.]{0,15}', '[at handle]', self)
        hand = re.sub(r'^[\w@](?!.*?\.{2})[\w.]{1,28}[\w]$', '[at handle]', self)

        if anonymize:
            return hand
        else:
            print(hand)
            return True if hand != self else False

        #if hand:
        #    return True
        #return None

    def has_pii(self):
        return self.has_us_phone() or self.has_email() or self.has_ipv4() or self.has_ipv6() or self.has_name() or \
               self.has_street_address() or self.has_credit_card() or self.has_at_handle()


def read_data(filename: str):
    data = []
    with open(filename) as f:
        # Read one line from the file stripping off the \n
        for line in f:
            data.append(line.rstrip())
    return data


if __name__ == '__main__':
    data = read_data('sample_data.txt')
    print(data)
    print('---')
    #debug phone number anon
    pii_data = Pii('My phone number is 123-123-1234')
    print(pii_data.has_us_phone(True))
    


    pii_data = Pii('My phone number is 123-123-1234')
    print(pii_data)

    if pii_data.has_pii():
        print('There is PII data preset')
    else:
        print('No PII data detected')
