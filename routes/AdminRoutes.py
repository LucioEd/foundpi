# routes/MainRoutes.py
# routes/MainRoutes.py
import os
from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from Repositories.CategoriaRepo import CategoriaRepo
from Repositories.ProdutoRepo import ProdutoRepo
from models.Categoria import Categoria
from models.Produto import Produto
from util.security import gerar_token, validar_usuario_logado
from util.templateFilters import formatarData
from models.Usuario import Usuario
from models.Cliente import Cliente

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get('/adm', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("adm.html", {"request": request,})

@router.get('/admprodutos', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admprodutos.html", {"request": request,})

@router.get('/admprodutoadd', response_class=HTMLResponse)
async def root(request: Request):
    categorias = CategoriaRepo.obterTodos()
    return templates.TemplateResponse("admprodutoadd.html", {"request": request, 'categorias':categorias})

@router.post('/addProduto')
async def root(request: Request, nome: str = Form(...), estoque: int=Form(...), preco: float=Form(...), descricao: str=Form(...), categoria: int=Form(...), imagem: UploadFile=Form(...)):
    nome_arquivo_original = imagem.filename
    nome_raiz, extensao = os.path.splitext(nome_arquivo_original)
    nome_com_extensao = f"{nome_raiz}{extensao}"
    print(nome_com_extensao)
    produto = Produto(id = 0, idCategoria = categoria, nome = nome, descricao=descricao, estoque=estoque, preco=preco, imgProduto=nome_com_extensao)
    ProdutoRepo.inserir(produto)
    return RedirectResponse('/adm',status.HTTP_302_FOUND)

@router.get('/admprodutoalt', response_class=HTMLResponse)
async def altProduto(request: Request,pa: int = 1,tp: int = 10):
    if Cliente.admin:
        produtos = ProdutoRepo.obterTodos()
        produtos_excluir = ProdutoRepo.excluir()
        produtos_alterar = ProdutoRepo.alterar()
        filtro = False
        numProdutos = ProdutoRepo.obterPagina(pa, tp)
        totalPaginas = ProdutoRepo.obterQtdePaginas(tp)
        cliente = validar_usuario_logado(request)
        return templates.TemplateResponse("index.html",{ "request": request, "produtos": produtos, 'filtro': filtro ,"numProdutos":numProdutos,
        "totalPaginas": totalPaginas,
        "paginaAtual": pa,
        "tamanhoPagina": tp,
        'cliente': cliente})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.get('/admcategorias', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admcategorias.html", {"request": request,})

@router.get('/admcategoriaadd', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admcategoriaadd.html", {"request": request,})

@router.post('/addCategoria')
async def root(nome:str=Form(...)):
    novaCategoria = Categoria(id= 0, nome=nome)
    print(novaCategoria)
    CategoriaRepo.inserir(novaCategoria)
    return RedirectResponse('/adm',status_code=status.HTTP_302_FOUND)


@router.get('/admcategoriasalt', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admcategoriasalt.html", {"request": request,})


@router.get("/", response_class=HTMLResponse)
async def getIndex(request: Request,pa: int = 1,tp: int = 10):
    produtos = ProdutoRepo.obterTodos()
    categorias = CategoriaRepo.obterTodos()
    filtro = False
    numProdutos = ProdutoRepo.obterPagina(pa, tp)
    totalPaginas = ProdutoRepo.obterQtdePaginas(tp)
    cliente = validar_usuario_logado(request)
    return templates.TemplateResponse("index.html",{ "request": request, "produtos": produtos, "categorias": categorias, 'filtro': filtro ,"numProdutos":numProdutos,
    "totalPaginas": totalPaginas,
    "paginaAtual": pa,
    "tamanhoPagina": tp,
    'cliente': cliente})