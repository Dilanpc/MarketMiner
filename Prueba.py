class Linio(Products):
    def __init__(self):
        super().__init__(use_selenium=True)
        self.page_name = "Linio"
        self._CARD_DATA = [
            [{""}], # Atributos para nombre #DUDAS Y CONFIRMACIÓN 
            [{""}], # Atributos para precio
            [{""}], # Atributos para link
            {}, # Atributos excluidos para nombre
            {}, # Atributos excluidos para precio
            {}  # Atributos excluidos para link
        ]
        self._CARD_DATA2 = [
            [{"class":"primary line-clamp-3 pod-subTitle subTitle-rebrand"}], # Atributos para nombre
            [{"class":"primary medium normal line-height-22"}], # Atributos para precio
            [{"class":"pod pod-link"}], # Atributos para link  CONFIRMAR SI SÍ SE PUEDE USAR ESA CLASE
            {}, # Atributos excluidos para nombre
            {}, # Atributos excluidos para precio
            {}  # Atributos excluidos para link
        ]

    def search_products(self, product: str):
        super().search_products(f"https://linio.falabella.com.co/linio-co/search?Ntt={product}")

    def _compute_products(self):
        try:
            product_section: BeautifulSoup = self.find(class_="jsx-2749142148 search-results--products")
            if product_section == None: raise ValueNotFoundByAttr("No se encontró la sección de productos")
            card_list = product_section.find_all(attrs={"class":"search-results-4-grid grid-pod"})
            if len(card_list) == 0: raise ValueNotFoundByAttr("No se encontraron tarjetas de productos")

            for card in card_list: #Convierte todos los tags en objetos ProductCard
                self.products.append(ProductCard(card, *self._CARD_DATA2))
                self.products[-1].link = "https://linio.falabella.com.co/linio-co" + self.products[-1].link

            if len(self.products) == 0:
                raise ValueNotFoundByAttr("No se encontraron productos")
            
            return self.products

        except Exception as e:
            print(e)
            return None
    

