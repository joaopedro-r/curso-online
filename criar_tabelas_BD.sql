												
CREATE database IF NOT EXISTS `curso`;
USE `curso` ;

-- -----------------------------------------------------
-- Table `curso`.`tb_aluno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `curso`.`tb_aluno` (
  `id_aluno` INT NOT NULL auto_increment,
  `nome_aluno` VARCHAR(25) NOT NULL,
  `sobrenome_aluno` VARCHAR(25) NOT NULL,
  `telefone` INT(8) ZEROFILL NOT NULL,
  `nascimento` DATE NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `genero` VARCHAR(45) NULL,
  PRIMARY KEY (`id_aluno`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `curso`.`tb_professor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `curso`.`tb_professor` (
  `id_prof` INT NOT NULL AUTO_INCREMENT,
  `nome_prof` VARCHAR(45) NOT NULL,
  `sobrenome_prof` VARCHAR(25) NOT NULL,
  `telefone_prof` INT(8) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `genero` VARCHAR(1) NULL,
  `nascimento` DATE NOT NULL,
  `salario` FLOAT NOT NULL,
  PRIMARY KEY (`id_prof`),
  UNIQUE INDEX `telefone_prof_UNIQUE` (`telefone_prof` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `curso`.`td_categorias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `curso`.`td_categorias` (
  `id_categoria` INT(2) NOT NULL auto_increment,
  `categorias` VARCHAR(25) NOT NULL,
  PRIMARY KEY (`id_categoria`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `curso`.`tb_curso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `curso`.`tb_curso` (
  `id_curso` INT(2) ZEROFILL NOT NULL auto_increment,
  `nome_curso` VARCHAR(45) NOT NULL,
  `preco` INT(4) UNSIGNED NOT NULL,
  `alunos_formados` INT(5) NOT NULL,
  `idt_categoria` INT(2) NOT NULL,
  PRIMARY KEY (`id_curso`),
  INDEX `fk_td_materia_ta_categorias1_idx` (`idt_categoria` ASC) VISIBLE,
  CONSTRAINT `fk_td_materia_ta_categorias1`
    FOREIGN KEY (`idt_categoria`)
    REFERENCES `curso`.`td_categorias` (`id_categoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `curso`.`ta_curso_aluno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `curso`.`ta_curso_aluno` (
  `td_aluno_id_aluno` INT NOT NULL,
  `tb_curso_id_curso` INT(2) ZEROFILL NOT NULL,
  PRIMARY KEY (`td_aluno_id_aluno`, `tb_curso_id_curso`),
  INDEX `fk_td_aluno_has_tb_curso_tb_curso1_idx` (`tb_curso_id_curso` ASC) VISIBLE,
  INDEX `fk_td_aluno_has_tb_curso_td_aluno1_idx` (`td_aluno_id_aluno` ASC) VISIBLE,
  CONSTRAINT `fk_td_aluno_has_tb_curso_td_aluno1`
    FOREIGN KEY (`td_aluno_id_aluno`)
    REFERENCES `curso`.`tb_aluno` (`id_aluno`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_td_aluno_has_tb_curso_tb_curso1`
    FOREIGN KEY (`tb_curso_id_curso`)
    REFERENCES `curso`.`tb_curso` (`id_curso`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `curso`.`ta_professor_curso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `curso`.`ta_professor_curso` (
  `tb_professor_id_prof` INT NOT NULL,
  `tb_curso_id_curso` INT(2) ZEROFILL NOT NULL,
  PRIMARY KEY (`tb_professor_id_prof`, `tb_curso_id_curso`),
  INDEX `fk_tb_professor_has_tb_curso_tb_curso1_idx` (`tb_curso_id_curso` ASC) VISIBLE,
  INDEX `fk_tb_professor_has_tb_curso_tb_professor1_idx` (`tb_professor_id_prof` ASC) VISIBLE,
  CONSTRAINT `fk_tb_professor_has_tb_curso_tb_professor1`
    FOREIGN KEY (`tb_professor_id_prof`)
    REFERENCES `curso`.`tb_professor` (`id_prof`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_professor_has_tb_curso_tb_curso1`
    FOREIGN KEY (`tb_curso_id_curso`)
    REFERENCES `curso`.`tb_curso` (`id_curso`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

insert into td_categorias (categorias) value
('Tecnologia'),                 
('Historia'),                   
('Dublagem'),                   
('Teatro'),
('Artes'),
('Ciencias');                     
------------------------------------
insert into tb_curso (nome_curso, preco, alunos_formados, idt_categoria) values       
('Python','350','243','1'),     
('Historia Brasil','280','465','2'),
('Dublagem','300','400','3'),   
('Atuação','366','540','4'),
('Mysql server','345','453','1'),
('Geografia','250','531','2'),
('Pintura','300','640','5'),
('Quimica','250','250','6'),
('Escultura','400','460','5');
------------------------------------									
insert into tb_professor (nome_prof, sobrenome_prof, telefone_prof, email, genero, nascimento, salario) value												
('Paulo','Costa','35439872','paulo@gmail.com', 'M','1995-05-25',1000.00),	
('Iago','Pinto','98745632','iago@gmail.com', 'M','1994-09-21','2000.00'),		
('Eduardo','Leite','23456789','dudu@hotmail.com', 'M','1993-01-01',2500.00),	
('Daniel','Muian','15973648','daniel@hotmail.com','M' ,'1998-02-18',3000.00),
('Danilo','Furlan','15983748','danilo@hotmail.com', 'M','1994-06-06',1230.00),
('Felipe','Muian','63987845','Felipe@gmail.com', 'M','1994-05-12',2100.00),
('Leila','Kinha','87456210','Leila@hotmail.com', 'F','1995-07-13',5000.00),
('João','Ricardo','69781450','JRicardo@gmail.com', 'M','1991-08-08',3000.00),
('Thiago','Panda','14785236','Thiago@gmail.com', 'M','1996-05-04',1500.00);	
-- ----------------------------------------------------					
insert into tb_aluno (nome_aluno, sobrenome_aluno, telefone, nascimento, email, genero) value												
('Ricardo','Juarez','87427821','2005-12-31', 'ricardo@gmail.com','M'),				
('Gabriela','Monteiro','33218181','2007-05-25', 'Gabriela@gmail.com','F'),			
('Italo','Fans','85412396','2004-09-21', 'italo@gmail.com','M'),					
('Diegue','Kawakami','47896520','2003-05-07', 'd2i@gmail.com',null),				
('Gustav','Fischer','33213030','2004-03-20', 'gustavrusso@gmail.com','M'),				
('Luscov','Boranov','87126352','2005-06-21', 'luscovrusso@gmail.com','M'),				
('Juliana','Ababoru','98127800','2002-05-07', 'juju123@gmail.com','F'),				
('Patricia','Abravan','41567893','2002-09-04', 'patyzianha@gmail.com','F'),
('Naian','Papão','87341241','2001-12-13', 'flavinhodopneu@gmail.com',null),				
('Fabio','Machado','33476140','2007-02-23', 'fabao@gmail.com','M'),			
('Eric','Thamais','85417656','2004-01-25', 'ericm@gmail.com','M'),					
('Lucas','Oliver','47896789','2003-09-06', 'luscassss@gmail.com',null),				
('Nathan','Pardal','3321170','2004-08-20', 'nath234@gmail.com','M'),				
('João','dos Anjos','87127892','2005-06-12', 'jotoso@gmail.com','M'),				
('Felipe','Talvez','08217654','2002-05-09', 'felipex@gmail.com','M'),				
('Luciano','Magralhoes','67927893','2002-07-04', 'lulunaololo@gmail.com',null),
('Julia','loura','37847861','2001-06-27', 'jujusala@gmail.com','F'),				
('Camila','Camomila','87125241','2003-02-10', 'camomila@gmail.com','F'),				
('Olivia','Oliveira','76540800','2004-03-19', 'olipalito@gmail.com','F'),				
('Eduarda','Duarte','76537893','2005-11-25', 'eduardaaa1233@gmail.com',null),
('Maria','Fiona','3524170','2004-08-20', 'mariaant@gmail.com','F'),
('Iago','Marçon','35747892','2005-07-13', 'iago@hotmail.com','M'),
('Mariana','Filomena','94217374','2001-12-09', 'mary@hotmail.com','F'),
('Juliana','Santos','92120793','2002-08-04', 'julianaa23o@gmail.com','F'),
('Kelvin','Ulisses','37121261','2001-01-27', 'kelvionmars@gmail.com','M'),
('Arthur','Rosa','87122141','1999-02-09', 'arthrei@gmail.com','M'),
('Micael','Maia','7137800','1999-06-29', 'mijackson@gmail.com','M'),
('Luan','Duarte','29807893','2004-11-15', 'luanzinho93@gmail.com',null),
('Oliver','Funcar','71789654','2000-10-02', 'olivereuao@gmail.com','M'),
('Fernando','Santos','23503489','2003-10-15', 'f13sssado@gmail.com',null);			
-- -----------------------------------------------------
select * from tb_aluno;
select * from tb_curso;
insert into ta_curso_aluno value
(1,4),
(2,3),
(2,1),
(2,5),
(3,3),
(4,5),
(5,5),
(6,1),
(7,2),
(8,3),
(9,4),
(10,5),
(11,6),
(12,7),
(13,8),
(14,9),
(15,2),
(16,3),
(17,3),
(18,4),
(19,5),
(20,6),
(21,7),
(22,8),
(23,9),
(24,1),
(25,2),
(26,3),
(27,4),
(28,5),
(29,6),
(30,7),
(30,8),
(22,9),
(15,1),
(16,2),
(11,3);
-- -----------------------------------------------------
insert into ta_professor_curso value
(2,4),
(2,3),
(2,1),
(2,2),
(3,3),
(4,5),
(5,5),
(6,1),
(7,2),
(8,3),
(9,4),
(1,5),
(2,6),
(3,7),
(4,8),
(5,9),
(6,2),
(6,3),
(7,3),
(1,4),
(2,5),
(1,6);