-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           5.7.31 - MySQL Community Server (GPL)
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              12.0.0.6468
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Copiando estrutura do banco de dados para garage_link_novo
DROP DATABASE IF EXISTS `garage_link_novo`;
CREATE DATABASE IF NOT EXISTS `garage_link_novo` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `garage_link_novo`;

-- Copiando estrutura para tabela garage_link_novo.avaria
DROP TABLE IF EXISTS `avaria`;
CREATE TABLE IF NOT EXISTS `avaria` (
  `id_avaria` int(11) NOT NULL AUTO_INCREMENT,
  `descricao_avaria` varchar(150) NOT NULL,
  `observacao_avaria` varchar(150) NOT NULL,
  `excluido_avaria` tinyint(1) DEFAULT '0',
  `placa_veiculo_placa` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`id_avaria`),
  KEY `avaria_FK` (`placa_veiculo_placa`),
  CONSTRAINT `avaria_FK` FOREIGN KEY (`placa_veiculo_placa`) REFERENCES `veiculo` (`placa_veiculo`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela garage_link_novo.avaria: ~2 rows (aproximadamente)
DELETE FROM `avaria`;
INSERT INTO `avaria` (`id_avaria`, `descricao_avaria`, `observacao_avaria`, `excluido_avaria`, `placa_veiculo_placa`) VALUES
	(1, 'teste', 'teste', 0, 'BPO1288'),
	(2, 'teste', 'teste', 1, 'BPO1288');

-- Copiando estrutura para tabela garage_link_novo.cliente
DROP TABLE IF EXISTS `cliente`;
CREATE TABLE IF NOT EXISTS `cliente` (
  `id_cliente` int(11) NOT NULL AUTO_INCREMENT,
  `cpf_cliente` varchar(11) NOT NULL,
  `nome_cliente` varchar(100) NOT NULL,
  `data_nascimento_cliente` date NOT NULL,
  `data_cadastro_cliente` date NOT NULL,
  `telefone_cliente` varchar(10) DEFAULT NULL,
  `celular_cliente` varchar(11) DEFAULT NULL,
  `email_cliente` varchar(100) DEFAULT NULL,
  `tipo_cliente` varchar(50) NOT NULL,
  `situacao_cliente` varchar(50) NOT NULL,
  `excluido_cliente` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela garage_link_novo.cliente: ~11 rows (aproximadamente)
DELETE FROM `cliente`;
INSERT INTO `cliente` (`id_cliente`, `cpf_cliente`, `nome_cliente`, `data_nascimento_cliente`, `data_cadastro_cliente`, `telefone_cliente`, `celular_cliente`, `email_cliente`, `tipo_cliente`, `situacao_cliente`, `excluido_cliente`) VALUES
	(1, '12092455079', 'Marcos Vinicius', '1990-10-10', '2020-10-11', '', '11980504246', 'marcos@hotmail.com', 'mensalista', 'em dia', 0),
	(3, '00760544034', 'José Antonio', '1991-10-10', '2020-10-12', '111111111', '11111111111', 'jose@hotmail.com', 'mensalista', 'em dia', 0),
	(4, '37726017074', 'Maria Silva', '1992-10-10', '2020-10-12', '111111111', '11111111111', 'maria@hotmail.com', 'mensalista', 'em dia', 0),
	(5, '89096739078', 'Juan Felipe', '1993-10-10', '2020-10-12', '111111111', '11111111111', 'juan@hotmail.com', 'mensalista', 'em dia', 0),
	(6, '53095292090', 'Diego Queiroz', '1994-10-10', '2020-10-12', '111111111', '11111111111', 'rafael@hotmail.com', 'mensalista', 'em dia', 0),
	(7, '81030269050', 'Rafael Reis', '1995-10-10', '2020-10-12', '111111111', '11111111111', 'teste@teste.com', 'mensalista', 'em dia', 0),
	(8, '50196165083', 'Leonardo Mancini', '1996-10-10', '2020-10-12', '111111111', '11111111111', 'teste@teste.com', 'mensalista', 'em dia', 0),
	(9, '78349954051', 'Kelvin Rodrigues', '1997-10-10', '2020-10-12', '111111111', '11111111111', 'teste@teste.com', 'mensalista', 'em dia', 0),
	(11, '12345678910', 'Ester Monteiro', '1970-03-10', '2020-10-13', '', '11953642658', 'ester@hotmail.com', 'mensalista', 'Em dia', 0),
	(21, '12345678910', 'Igor Ramos', '2000-10-13', '2020-10-13', ' ', ' ', ' ', 'único', 'em dia', 0),
	(31, '12345678910', 'Débora Freitas', '2000-01-31', '2020-10-13', ' ', ' ', ' ', 'único', 'em dia', 0);

-- Copiando estrutura para tabela garage_link_novo.estacionamento
DROP TABLE IF EXISTS `estacionamento`;
CREATE TABLE IF NOT EXISTS `estacionamento` (
  `id_estacionamento` int(11) NOT NULL AUTO_INCREMENT,
  `entrada_estacionamento` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `saida_estacionamento` timestamp NULL DEFAULT NULL,
  `observacao_estacionamento` varchar(100) DEFAULT NULL,
  `valor_liquido_estacionamento` float DEFAULT '0',
  `valor_total_estacionamento` float NOT NULL DEFAULT '0',
  `valor_recebido_estacionamento` float DEFAULT '0',
  `desconto_estacionamento` float DEFAULT '0',
  `tipo_pagamento_estacionamento` varchar(30) DEFAULT NULL,
  `situacao_estacionamento` varchar(30) NOT NULL,
  `excluido_estacionamento` tinyint(1) NOT NULL DEFAULT '0',
  `veiculo_placa_veiculo` varchar(8) NOT NULL,
  `vaga_id_vaga` int(11) NOT NULL,
  PRIMARY KEY (`id_estacionamento`),
  KEY `estacionamento_FK` (`veiculo_placa_veiculo`),
  KEY `estacionamento_FK_1` (`vaga_id_vaga`),
  CONSTRAINT `estacionamento_FK` FOREIGN KEY (`veiculo_placa_veiculo`) REFERENCES `veiculo` (`placa_veiculo`),
  CONSTRAINT `estacionamento_FK_1` FOREIGN KEY (`vaga_id_vaga`) REFERENCES `vaga` (`id_vaga`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela garage_link_novo.estacionamento: ~12 rows (aproximadamente)
DELETE FROM `estacionamento`;
INSERT INTO `estacionamento` (`id_estacionamento`, `entrada_estacionamento`, `saida_estacionamento`, `observacao_estacionamento`, `valor_liquido_estacionamento`, `valor_total_estacionamento`, `valor_recebido_estacionamento`, `desconto_estacionamento`, `tipo_pagamento_estacionamento`, `situacao_estacionamento`, `excluido_estacionamento`, `veiculo_placa_veiculo`, `vaga_id_vaga`) VALUES
	(33, '2020-11-05 00:48:04', NULL, 'teste x', 95, 95, 95, 0, 'Dinheiro', 'pago', 1, 'BPO1288', 1),
	(34, '2020-11-12 23:11:32', NULL, 'teste', 65, 65, 15, 0, 'Dinheiro', 'pendente', 1, 'DGE2138', 1),
	(35, '2020-11-13 02:11:32', '2020-11-13 02:16:06', 'teste', 15, 15, 15, 0, 'Dinheiro', 'pago', 0, 'BPO1288', 1),
	(36, '2020-11-14 23:54:43', NULL, '', 30, 30, NULL, NULL, NULL, 'pendente', 1, 'BPO1288', 1),
	(37, '2020-11-15 01:12:31', '2020-11-15 01:20:26', '', 31.75, 31.75, 31.75, 0, 'Dinheiro', 'pago', 0, 'BPO1288', 1),
	(38, '2020-11-15 01:38:43', NULL, '', 4.75, 4.75, 10, 0, 'Dinheiro', 'pendente', 1, 'BPO1288', 1),
	(39, '2020-11-15 02:50:00', NULL, '', 0, 0, 0, 0, 'Dinheiro', 'pago', 1, 'BPO1288', 1),
	(40, '2020-11-15 02:55:00', NULL, 'teste', 0, 0, NULL, NULL, NULL, 'pendente', 1, 'BPO1288', 1),
	(41, '2020-11-15 03:20:47', NULL, '', -80, -80, NULL, NULL, NULL, 'pendente', 1, 'BPO1288', 1),
	(42, '2020-11-15 03:44:23', NULL, 'teste', 80, 80, NULL, NULL, NULL, 'pendente', 1, 'BPO1288', 1),
	(43, '2020-11-15 03:47:11', '2020-11-15 03:48:29', 'teste', 50, 50, 50, 0, 'Dinheiro', 'pago', 0, 'BPO1288', 1),
	(44, '2020-11-15 03:51:03', '2020-11-15 03:51:06', 'teste', 0, 0, 0, 0, 'Dinheiro', 'pago', 0, 'BPO1288', 1);

-- Copiando estrutura para tabela garage_link_novo.funcionario
DROP TABLE IF EXISTS `funcionario`;
CREATE TABLE IF NOT EXISTS `funcionario` (
  `id_funcionario` int(11) NOT NULL AUTO_INCREMENT,
  `nome_funcionario` varchar(100) NOT NULL,
  `cpf_funcionario` varchar(11) NOT NULL,
  `telefone_funcionario` varchar(10) DEFAULT NULL,
  `celular_funcionario` varchar(11) NOT NULL,
  `endereco_funcionario` varchar(100) NOT NULL,
  `tipo_funcionario` varchar(50) NOT NULL,
  `excluido_funcionario` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_funcionario`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela garage_link_novo.funcionario: ~9 rows (aproximadamente)
DELETE FROM `funcionario`;
INSERT INTO `funcionario` (`id_funcionario`, `nome_funcionario`, `cpf_funcionario`, `telefone_funcionario`, `celular_funcionario`, `endereco_funcionario`, `tipo_funcionario`, `excluido_funcionario`) VALUES
	(1, 'Juan Felipe', '20688009000', 'N/A', '11111111111', 'Rua 1', 'atendente', 0),
	(2, 'Admin', '48685123854', 'N/A', '11845236781', 'Avenida 2', 'gerente', 0),
	(3, 'Rafael Reis', '97685426080', 'N/A', '11111111111', 'Avenida 3', 'atendente', 0),
	(4, 'Leonardo Mancini', '30412057000', 'N/A', '11111111111', 'Rua 4', 'atendente', 0),
	(5, 'Kelvin Rodrigues', '20725340037', 'N/A', '11111111111', 'Avenida 5', 'atendente', 0),
	(6, 'Diego Queiroz', '17161810035', 'N/A', '11111111111', 'Rua 3', 'atendente', 0),
	(7, 'teste', '49086658008', 'teste', 'teste', 'Rua 1', 'atendente', 1),
	(11, 'Marcia Mendes', '12345678910', '1155781687', '11953742657', '', 'atendente', 1),
	(12, 'Novo Funcionario', '45612345678', '1185461235', '11985461235', '', 'gerente', 0);

-- Copiando estrutura para tabela garage_link_novo.mensalidade
DROP TABLE IF EXISTS `mensalidade`;
CREATE TABLE IF NOT EXISTS `mensalidade` (
  `id_mensalidade` int(11) NOT NULL AUTO_INCREMENT,
  `valor_mensalidade` float NOT NULL DEFAULT '0',
  `data_vencimento_mensalidade` date NOT NULL,
  `data_pagamento_mensalidade` date NOT NULL,
  `situacao_mensalidade` varchar(30) NOT NULL DEFAULT '',
  `excluido_mensalidade` tinyint(1) NOT NULL DEFAULT '0',
  `cliente_id_cliente` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_mensalidade`),
  KEY `mensalidade_FK` (`cliente_id_cliente`),
  CONSTRAINT `mensalidade_FK` FOREIGN KEY (`cliente_id_cliente`) REFERENCES `cliente` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela garage_link_novo.mensalidade: ~4 rows (aproximadamente)
DELETE FROM `mensalidade`;
INSERT INTO `mensalidade` (`id_mensalidade`, `valor_mensalidade`, `data_vencimento_mensalidade`, `data_pagamento_mensalidade`, `situacao_mensalidade`, `excluido_mensalidade`, `cliente_id_cliente`) VALUES
	(1, 200, '2020-09-20', '2020-09-20', 'em aberto', 1, 1),
	(2, 20, '2020-11-24', '2020-10-24', 'pago', 1, NULL),
	(3, 30, '2020-10-20', '2020-10-20', 'pago', 0, 1),
	(4, 30, '2020-10-20', '2020-10-20', 'em aberto', 1, 1),
	(5, 30, '2020-10-20', '2020-10-20', 'em aberto', 1, 1);

-- Copiando estrutura para tabela garage_link_novo.servico
DROP TABLE IF EXISTS `servico`;
CREATE TABLE IF NOT EXISTS `servico` (
  `id_servico` int(11) NOT NULL AUTO_INCREMENT,
  `nome_servico` varchar(50) DEFAULT NULL,
  `descricao_servico` varchar(100) NOT NULL,
  `situacao_servico` varchar(30) DEFAULT NULL,
  `preco_servico` float NOT NULL DEFAULT '0',
  `tipo_servico` varchar(30) NOT NULL,
  `excluido_servico` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_servico`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela garage_link_novo.servico: ~3 rows (aproximadamente)
DELETE FROM `servico`;
INSERT INTO `servico` (`id_servico`, `nome_servico`, `descricao_servico`, `situacao_servico`, `preco_servico`, `tipo_servico`, `excluido_servico`) VALUES
	(7, 'Estacionamento', 'estacionamento', 'ativo', 10, 'estacionamento', 1),
	(8, 'Troca de oleo', 'troca de oleo', 'ativo', 50, 'servico', 0),
	(9, 'Lavagem', 'lavagem', 'ativo', 30, 'servico', 0),
	(10, 'Estacionamento Hora', 'Cobrar por hora', 'ativo', 15, 'estacionamento', 0);

-- Copiando estrutura para tabela garage_link_novo.servico_estacionamento
DROP TABLE IF EXISTS `servico_estacionamento`;
CREATE TABLE IF NOT EXISTS `servico_estacionamento` (
  `id_servico_estacionamento` int(11) NOT NULL AUTO_INCREMENT,
  `estacionamento_id_estacionamento` int(11) NOT NULL,
  `servico_id_servico` int(11) NOT NULL,
  `nome_servico` varchar(50) NOT NULL DEFAULT '',
  `preco_servico` float NOT NULL DEFAULT '0',
  `excluido_servico` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_servico_estacionamento`) USING BTREE,
  KEY `servico_estacionamento_FK_1` (`servico_id_servico`),
  KEY `servico_estacionamento_FK` (`estacionamento_id_estacionamento`),
  CONSTRAINT `servico_estacionamento_FK` FOREIGN KEY (`estacionamento_id_estacionamento`) REFERENCES `estacionamento` (`id_estacionamento`),
  CONSTRAINT `servico_estacionamento_FK_1` FOREIGN KEY (`servico_id_servico`) REFERENCES `servico` (`id_servico`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela garage_link_novo.servico_estacionamento: ~21 rows (aproximadamente)
DELETE FROM `servico_estacionamento`;
INSERT INTO `servico_estacionamento` (`id_servico_estacionamento`, `estacionamento_id_estacionamento`, `servico_id_servico`, `nome_servico`, `preco_servico`, `excluido_servico`) VALUES
	(1, 37, 9, 'Lavagem', 30, 1),
	(2, 37, 10, 'Estacionamento Hora', 15, 1),
	(3, 38, 10, 'Estacionamento Hora', 15, 1),
	(4, 39, 10, 'Estacionamento Hora', 15, 1),
	(5, 40, 10, 'Estacionamento Hora', 15, 1),
	(6, 40, 9, 'Lavagem', 30, 1),
	(7, 40, 9, 'Lavagem', 30, 1),
	(8, 41, 10, 'Estacionamento Hora', 15, 1),
	(9, 41, 9, 'Lavagem', 30, 1),
	(10, 41, 9, 'Lavagem', 30, 1),
	(11, 41, 9, 'Lavagem', 30, 1),
	(12, 42, 10, 'Estacionamento Hora', 15, 1),
	(13, 42, 8, 'Troca de oleo', 50, 1),
	(14, 42, 9, 'Lavagem', 30, 1),
	(15, 42, 8, 'Troca de oleo', 50, 1),
	(16, 42, 9, 'Lavagem', 30, 1),
	(17, 43, 10, 'Estacionamento Hora', 15, 0),
	(18, 43, 9, 'Lavagem', 30, 1),
	(19, 43, 8, 'Troca de oleo', 50, 0),
	(20, 43, 9, 'Lavagem', 30, 0),
	(21, 43, 8, 'Troca de oleo', 50, 0),
	(22, 44, 10, 'Estacionamento Hora', 15, 0),
	(23, 44, 8, 'Troca de oleo', 50, 1);

-- Copiando estrutura para tabela garage_link_novo.usuario
DROP TABLE IF EXISTS `usuario`;
CREATE TABLE IF NOT EXISTS `usuario` (
  `login_usuario` varchar(50) NOT NULL,
  `nome_usuario` varchar(100) NOT NULL,
  `email_usuario` varchar(100) NOT NULL,
  `senha_usuario` varchar(200) NOT NULL,
  `tipo_usuario` varchar(20) NOT NULL,
  `situacao_usuario` varchar(20) NOT NULL DEFAULT 'ativo',
  `excluido_usuario` tinyint(1) NOT NULL DEFAULT '0',
  `funcionario_id_funcionario` int(11) NOT NULL,
  PRIMARY KEY (`login_usuario`) USING BTREE,
  KEY `usuario_FK` (`funcionario_id_funcionario`),
  CONSTRAINT `usuario_FK` FOREIGN KEY (`funcionario_id_funcionario`) REFERENCES `funcionario` (`id_funcionario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela garage_link_novo.usuario: ~5 rows (aproximadamente)
DELETE FROM `usuario`;
INSERT INTO `usuario` (`login_usuario`, `nome_usuario`, `email_usuario`, `senha_usuario`, `tipo_usuario`, `situacao_usuario`, `excluido_usuario`, `funcionario_id_funcionario`) VALUES
	('admin', 'Administrador', 'admin@hotmail.com', 'pbkdf2:sha256:150000$Ozs07v0l$f12605f9814133bbc2c8f9b8c9b3cfbb529d701eb77e76c20bd801040a9ec682', 'gerente', 'ativo', 0, 2),
	('diego', 'Diego Queiroz', 'diego@hotmail.com', 'pbkdf2:sha256:150000$jvpnvfQM$19d89ce0f2835b2cdf09fbad031d95d5df20167831bcb82152e14b2bac8f1a5e', 'atendente', 'ativo', 1, 4),
	('juan', 'Juan Felipe', 'juan@hotmail.com', 'pbkdf2:sha256:150000$rImEhbMy$ff3f22858924c92bd4da099133925743afa8da7bafda4b1de817959d9e44dd67', 'atendente', 'ativo', 0, 1),
	('novo', 'Novo Usuario', 'usuario@hotmail.com', 'pbkdf2:sha256:150000$1DWCHxkq$d4359868a4c16472abb81ca9169183aad79e51ec2720cce04d0daf0f83f2c997', 'gerente', 'ativo', 0, 12),
	('rafael', 'Rafael Reis', 'rafael@hotmail.com', 'pbkdf2:sha256:150000$r71d2xVV$c92337f4afcdf94e984d66fe01220bd875cb8d7b86b3a68420cbe5de1010f373', 'atendente', 'ativo', 0, 3),
	('teste', 'teste', 'teste', 'pbkdf2:sha256:150000$dYqaNCh1$7c5e3ca4e0283ed92bab1bd3faaca4fbae6d592659782dec3cc2e07b2bdb6b55', 'atendente', 'ativo', 1, 7);

-- Copiando estrutura para tabela garage_link_novo.usuario_estacionamento
DROP TABLE IF EXISTS `usuario_estacionamento`;
CREATE TABLE IF NOT EXISTS `usuario_estacionamento` (
  `estacionamento_id_estacionamento` int(11) NOT NULL,
  `usuario_login_usuario` varchar(50) NOT NULL,
  `excluido_usuario` int(11) DEFAULT '0',
  PRIMARY KEY (`estacionamento_id_estacionamento`,`usuario_login_usuario`),
  KEY `usuario_estacionamento_FK_1` (`usuario_login_usuario`),
  CONSTRAINT `usuario_estacionamento_FK` FOREIGN KEY (`estacionamento_id_estacionamento`) REFERENCES `estacionamento` (`id_estacionamento`),
  CONSTRAINT `usuario_estacionamento_FK_1` FOREIGN KEY (`usuario_login_usuario`) REFERENCES `usuario` (`login_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela garage_link_novo.usuario_estacionamento: ~12 rows (aproximadamente)
DELETE FROM `usuario_estacionamento`;
INSERT INTO `usuario_estacionamento` (`estacionamento_id_estacionamento`, `usuario_login_usuario`, `excluido_usuario`) VALUES
	(33, 'admin', 1),
	(34, 'admin', 1),
	(35, 'admin', 0),
	(36, 'admin', 1),
	(37, 'admin', 0),
	(38, 'admin', 1),
	(39, 'admin', 1),
	(40, 'admin', 1),
	(41, 'admin', 1),
	(42, 'admin', 1),
	(43, 'admin', 0),
	(44, 'admin', 0);

-- Copiando estrutura para tabela garage_link_novo.vaga
DROP TABLE IF EXISTS `vaga`;
CREATE TABLE IF NOT EXISTS `vaga` (
  `id_vaga` int(11) NOT NULL AUTO_INCREMENT,
  `localizacao_vaga` varchar(50) NOT NULL,
  `codigo_vaga` varchar(10) NOT NULL,
  `situacao_vaga` varchar(50) NOT NULL,
  `excluido_vaga` tinyint(1) NOT NULL DEFAULT '0',
  `veiculo_placa_veiculo` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`id_vaga`),
  KEY `vaga_FK` (`veiculo_placa_veiculo`),
  CONSTRAINT `vaga_FK` FOREIGN KEY (`veiculo_placa_veiculo`) REFERENCES `veiculo` (`placa_veiculo`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela garage_link_novo.vaga: ~3 rows (aproximadamente)
DELETE FROM `vaga`;
INSERT INTO `vaga` (`id_vaga`, `localizacao_vaga`, `codigo_vaga`, `situacao_vaga`, `excluido_vaga`, `veiculo_placa_veiculo`) VALUES
	(1, 'Térreo', 'TR001', 'livre', 0, NULL),
	(2, 'Térreo', 'TR002', 'livre', 0, NULL),
	(3, 'Térreo', 'ABC x', 'livre', 1, NULL);

-- Copiando estrutura para tabela garage_link_novo.veiculo
DROP TABLE IF EXISTS `veiculo`;
CREATE TABLE IF NOT EXISTS `veiculo` (
  `placa_veiculo` varchar(8) NOT NULL,
  `modelo_veiculo` varchar(50) NOT NULL,
  `marca_veiculo` varchar(50) NOT NULL,
  `cor_veiculo` varchar(50) NOT NULL,
  `ano_fabricacao_veiculo` year(4) NOT NULL,
  `ano_modelo_veiculo` year(4) NOT NULL,
  `excluido_veiculo` tinyint(1) NOT NULL DEFAULT '0',
  `cliente_id_cliente` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`placa_veiculo`),
  KEY `veiculo_FK` (`cliente_id_cliente`),
  CONSTRAINT `veiculo_FK` FOREIGN KEY (`cliente_id_cliente`) REFERENCES `cliente` (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela garage_link_novo.veiculo: ~2 rows (aproximadamente)
DELETE FROM `veiculo`;
INSERT INTO `veiculo` (`placa_veiculo`, `modelo_veiculo`, `marca_veiculo`, `cor_veiculo`, `ano_fabricacao_veiculo`, `ano_modelo_veiculo`, `excluido_veiculo`, `cliente_id_cliente`) VALUES
	('BPO1288', 'CG 160 Start', 'Honda', 'Preta', '2018', '2019', 0, 1),
	('DGE2138', 'Palio Fire', 'FIAT', 'Cinza', '2001', '2001', 0, 3);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
