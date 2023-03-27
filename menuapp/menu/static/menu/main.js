
class Menu {

  constructor() {
  }
  
  #getRoots() {
    const urlParams = new URLSearchParams(window.location.search);
    
    const uls = document.getElementsByClassName('menu-root')
    const params = {}
    
    for (let index = 0; index < uls.length; index++) {
      const rid = uls[index].getAttribute('name');
      const qs = urlParams.get(rid)
      if (qs !== null){
        if (params[qs] === undefined)
          params[qs] = []
        params[qs].push(uls[index])
      }
    }
    return params;
  }

  #setActiveItem([key,val]){
    for (const ti of val) {
      const vi = ti.querySelector('.menu__li > .menu')
      if (vi === null)
        continue
      console.log(vi)
      const splits = new Set(key.split('/'))
      const t = [vi,...vi.getElementsByClassName('menu')]
      console.log(t)
      t.forEach(v => {
        const tmp = v.getAttribute('name')
        if (splits.has(tmp)) {
          v.classList.add('active')
          v.parentElement.querySelector('.menu__summary > .menu__caret').classList.toggle("menu__caret-down")
        }
      })
      
    }
  }

  #addListeners(){
    let toggler = document.getElementsByClassName("menu__caret");
    for (let i = 0; i < toggler.length; i++) {
      toggler[i].addEventListener("click", function() {
        this.parentElement.parentElement
          .querySelector('.menu__li > .menu')?.classList.toggle("active");
        this.classList.toggle("menu__caret-down");
      });
    }
  }

  start() {
    const params = this.#getRoots()
    Object.entries(params).forEach(p => this.#setActiveItem(p))
    this.#addListeners()
  }
}


document.addEventListener('DOMContentLoaded', () => (new Menu()).start(),false)