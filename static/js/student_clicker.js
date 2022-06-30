function clickHP() {
    HPval.innerHTML = parseInt(HPval.innerHTML) + 4;
    console.log('HP', HPval.innerHTML);
}
function clickIQ() {
    IQval.innerHTML = parseInt(IQval.innerHTML) + 6;
    console.log('IQ', IQval.innerHTML);
}
function clickHappiness() {
    Happval.innerHTML = parseInt(Happval.innerHTML) + 3;
    console.log('Happ', Happval.innerHTML);
}
function makeAllGood() {
    HPval.innerHTML = parseInt(HPval.innerHTML) + 4;
    IQval.innerHTML = parseInt(IQval.innerHTML) + 4;
    Happval.innerHTML = parseInt(Happval.innerHTML) + 4;
}
function preSubmit() {
    allE.value = HPval.innerHTML + '*' + IQval.innerHTML + '*' + Happval.innerHTML;
}