// Avaliacoes de uma empresa com nota maior do que 5
db.avaliacoesEmpresas.aggregate([
    { $match: { "nome": "Sedex" } },
    { $unwind: "$avaliacoes" },
    { $match: { "avaliacoes.nota": { $gte: 5 } } },
]);

// Nome das empresas e o dos usuarios que deram nota menor do que 4
db.avaliacoesEmpresas.aggregate([
    { $unwind: "$avaliacoes" },
    { $match: { "avaliacoes.nota": { $lte: 4 } } },
    {
        $project: {
            _id: 0,
            nome: 1,
            nota: "$avaliacoes.nota",
            usuario: "$avaliacoes.usuario.nome"
        }
    }
]);

// Media das notas de todas as empresas
db.avaliacoesEmpresas.aggregate([
    { $unwind: "$avaliacoes" },
    { $group: {
        _id: "$_id",
        avg_nota: { $avg: "$avaliacoes.nota" }
    }}
]);

// Avaliacoes antes de determinada data
db.avaliacoesEmpresas.aggregate([
    { $unwind: "$avaliacoes" },
    { $match: { "avaliacoes.data": { $lte: { "$date": { "$numberLong": "1355314332000" }}}}}
])

// Quantidade de avaliacoes de um produto
db.avaliacoesProdutos.aggregate([
    { $unwind: "$avaliacoes" },
    { $group: {
        _id: "$_id",
        qtty: { $sum: 1 }
    }}
]);
