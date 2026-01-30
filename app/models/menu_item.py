class MenuItem:
    """Menu Item model for Firestore"""
    
    def __init__(self, item_id, name, description, price, category, image_url=None, available=True):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.image_url = image_url
        self.available = available
    
    def to_dict(self):
        return {
            'item_id': self.item_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'image_url': self.image_url,
            'available': self.available
        }
    
    @staticmethod
    def from_dict(data):
        return MenuItem(
            item_id=data.get('item_id'),
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            category=data.get('category'),
            image_url=data.get('image_url'),
            available=data.get('available', True)
        )