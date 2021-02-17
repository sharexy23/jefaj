def json(self):
    return {'phone_number':self.phone_number,'firstname':self.firstname,'middlename':self.middlename,'lastname':self.lastname,'date_of_birth':self.date_of_birth,'password':self.password,'email':self.email,'pin':self.pin,'account_balance':self.account_balance,'transfers':[transfer.json() for transfer in self.transfers.all()]}
