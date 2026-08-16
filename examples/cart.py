from ux_app import App, Badge, Component


class CartBadge(Component):
    id = "cart.badge"
    count: int = 0

    def render(self):
        return Badge(self.count, on_click=self.add)

    def add(self, sku: str = ""):
        self.count += 1


app = App.boot(title="Cart")
app.add(CartBadge)

if __name__ == "__main__":
    print(app.html("cart.badge"))
    app.click("cart.badge")
    print(app.world.ui["cart.badge"])
