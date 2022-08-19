-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 192.168.1.3
-- Время создания: Авг 18 2022 г., 22:45
-- Версия сервера: 8.0.30
-- Версия PHP: 8.0.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `21_passbot`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Passes`
--

CREATE TABLE `Passes` (
  `pass_id` int NOT NULL,
  `inviter_id` text NOT NULL,
  `guest_name` text NOT NULL,
  `start_datetime` datetime NOT NULL,
  `duration` int NOT NULL,
  `status` int NOT NULL,
  `campus` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `temp`
--

CREATE TABLE `temp` (
  `user_id` text NOT NULL,
  `state` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `temp`
--

INSERT INTO `temp` (`user_id`, `state`) VALUES
('766274883', 2),
('278691095', 2),
('766274883', 0);

-- --------------------------------------------------------

--
-- Структура таблицы `Users`
--

CREATE TABLE `Users` (
  `user_id` text NOT NULL,
  `nickname` text NOT NULL,
  `full_name` text NOT NULL,
  `email` text NOT NULL,
  `role` int NOT NULL,
  `campus` int NOT NULL,
  `state` int NOT NULL,
  `code` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Users`
--

INSERT INTO `Users` (`user_id`, `nickname`, `full_name`, `email`, `role`, `campus`, `state`, `code`) VALUES
('1935966096', 'ftonita', 'phylantrophist ftonita', 'ftonita@student.21-school.ru', 1, 2, 4, 215748),
('189380149', 'bmarilli', 'Набияров Фанзиль Фандузович', 'bmarilli@student.21-school.ru', 1, 2, 4, 489644);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
