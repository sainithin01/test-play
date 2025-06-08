class CarMan:
    def __init__(self, model_type, colour, price):
        self.model_type = model_type
        self.colour = colour
        self.price = price

    def discount_for_black(self):
        if self.colour == "Black":
           discounted_price = self.price*0.9
           print(f"Yayy!! You get a freaking discount. Final Price is ${discounted_price}")
    
    def car_not_found_404(self):
        if self.model_type == "i20":
            print("We don't have the car you're looking for, sorry bro")


if __name__ == "__main__":
    mycar = CarMan("Suzuki", "Black", 25000)
    mycar.discount_for_black()