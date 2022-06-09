const list = [1, 2, 3];
renderItem = () => {
  list.forEach((element) => {
    var newEl = document.createElement('div');
    newEl.innerHTML = `
    <div class="page__content__item" id=${element.toString()}>
      <div class="avt" style="background-image: url('https://tse3.mm.bing.net/th?id=OIP.GlFTKon5rkQNZkoUL2k_0QHaHa&pid=Api&P=0&w=185&h=185');"></div>
      <div style="margin-left: 40px; display: grid">
        <span>Name ${element}</span>
        <span>Role</span>
        <span>Full name</span>
        <span>Student code</span>
      </div>
    </div>
    `;
    document.getElementById('pageContent').appendChild(newEl);
  });
};

renderItem();
