package view
{
    import flash.display.*;
    import flash.filters.*;
    import flash.events.MouseEvent;
    import flash.events.Event;
    import flash.events.EventDispatcher;

    import mx.core.UIComponent;
    import mx.core.MovieClipLoaderAsset;
    import mx.events.StateChangeEvent;
    import mx.controls.Button;
    import mx.controls.Label;
    import mx.containers.Panel;

    import org.libspark.thread.*;
    import org.libspark.thread.utils.*;
    import org.libspark.thread.threads.between.BeTweenAS3Thread;

    import model.*;
    import model.events.*;

    import view.image.match.*;
    import view.utils.*;
    import view.scene.match.*;
    import view.scene.common.*;

    import net.server.LobbyServer;

    import controller.*;

    /**
     * マッチング画面のビュークラス
     *
     */
    public class MatchView extends Thread
    {
        // 翻訳データ
        CONFIG::LOCALE_JP
        private static const _TRANS_LOBBY	:String = "対戦ロビー";
        CONFIG::LOCALE_JP
        private static const _TRANS_ALERT	:String = "警告";
        CONFIG::LOCALE_JP
        private static const _TRANS_MSG1	:String = "デッキ枚数が異なります";
        CONFIG::LOCALE_JP
        private static const _TRANS_MSG2	:String = "APが足りません";

        CONFIG::LOCALE_EN
        private static const _TRANS_LOBBY	:String = "Battle Lobby";
        CONFIG::LOCALE_EN
        private static const _TRANS_ALERT	:String = "Warning";
        CONFIG::LOCALE_EN
        private static const _TRANS_MSG1	:String = "Deck size doesn't match.";
        CONFIG::LOCALE_EN
        private static const _TRANS_MSG2	:String = "Not enough AP.";

        CONFIG::LOCALE_TCN
        private static const _TRANS_LOBBY	:String = "對戰大廳";
        CONFIG::LOCALE_TCN
        private static const _TRANS_ALERT	:String = "警告";
        CONFIG::LOCALE_TCN
        private static const _TRANS_MSG1	:String = "牌組張數不同";
        CONFIG::LOCALE_TCN
        private static const _TRANS_MSG2	:String = "AP不足";

        CONFIG::LOCALE_SCN
        private static const _TRANS_LOBBY	:String = "对战大厅";
        CONFIG::LOCALE_SCN
        private static const _TRANS_ALERT	:String = "警告";
        CONFIG::LOCALE_SCN
        private static const _TRANS_MSG1	:String = "卡组张数不同";
        CONFIG::LOCALE_SCN
        private static const _TRANS_MSG2	:String = "AP不足";

        CONFIG::LOCALE_KR
        private static const _TRANS_LOBBY	:String = "대전 로비";
        CONFIG::LOCALE_KR
        private static const _TRANS_ALERT	:String = "경고";
        CONFIG::LOCALE_KR
        private static const _TRANS_MSG1	:String = "덱의 카드 수가 틀립니다.";
        CONFIG::LOCALE_KR
        private static const _TRANS_MSG2	:String = "AP가 부족합니다.";

        CONFIG::LOCALE_FR
        private static const _TRANS_LOBBY	:String = "Hall de Duels en ligne";
        CONFIG::LOCALE_FR
        private static const _TRANS_ALERT	:String = "Attention";
        CONFIG::LOCALE_FR
        private static const _TRANS_MSG1	:String = "Nombre incorrect de cartes dans la pioche";
        CONFIG::LOCALE_FR
        private static const _TRANS_MSG2	:String = "AP insuffisants";

        CONFIG::LOCALE_ID
        private static const _TRANS_LOBBY	:String = "対戦ロビー";
        CONFIG::LOCALE_ID
        private static const _TRANS_ALERT	:String = "警告";
        CONFIG::LOCALE_ID
        private static const _TRANS_MSG1	:String = "デッキ枚数が異なります";
        CONFIG::LOCALE_ID
        private static const _TRANS_MSG2	:String = "APが足りません";

        CONFIG::LOCALE_TH
        private static const _TRANS_LOBBY   :String = "ห้องรับรองการประลอง";
        CONFIG::LOCALE_TH
        private static const _TRANS_ALERT   :String = "คำเตือน";
        CONFIG::LOCALE_TH
        private static const _TRANS_MSG1    :String = "จำนวนไพ่ในสำรับต่างกัน";
        CONFIG::LOCALE_TH
        private static const _TRANS_MSG2    :String = "AP ไม่เพียงพอ";


        CONFIG::LOCALE_JP
        private static const _TRANS_COST_LIMIT_QUICK_MSG:String  = "デッキコストがチャンネルルールと一致していません";
        CONFIG::LOCALE_JP
        private static const _TRANS_COST_LIMIT_CREATE_MSG:String = "デッキコストがチャンネルルールに合わないため、作成できませんでした。";
        CONFIG::LOCALE_JP
        private static const _TRANS_COST_LIMIT_JOIN_MSG:String   = "デッキコストがチャンネルルールに合わないため、入室できませんでした。";

        CONFIG::LOCALE_EN
        private static const _TRANS_COST_LIMIT_QUICK_MSG:String  = "Could not enter because your deck cost does meet the channel requirements.";
        CONFIG::LOCALE_EN
        private static const _TRANS_COST_LIMIT_CREATE_MSG:String = "Could not proceed because your deck cost does meet the channel requirements.";
        CONFIG::LOCALE_EN
        private static const _TRANS_COST_LIMIT_JOIN_MSG:String   = "Could not enter the room because your deck cost does meet the channel requirements.";

        CONFIG::LOCALE_TCN
        private static const _TRANS_COST_LIMIT_QUICK_MSG:String  = "牌組COST與此區規定不合，所以無法入場。";
        CONFIG::LOCALE_TCN
        private static const _TRANS_COST_LIMIT_CREATE_MSG:String = "牌組COST與此區規定不合，所以無法編排。";
        CONFIG::LOCALE_TCN
        private static const _TRANS_COST_LIMIT_JOIN_MSG:String   = "牌組COST與此區規定不合，所以無法進房。";

        CONFIG::LOCALE_SCN
        private static const _TRANS_COST_LIMIT_QUICK_MSG:String  = "卡组成本不符合通道规则，因此无法进入。";
        CONFIG::LOCALE_SCN
        private static const _TRANS_COST_LIMIT_CREATE_MSG:String = "卡组成本不符合通道规则，因此无法编辑。";
        CONFIG::LOCALE_SCN
        private static const _TRANS_COST_LIMIT_JOIN_MSG:String   = "卡组成本不符合通道规则，因此无法进入对战室。";

        CONFIG::LOCALE_KR
        private static const _TRANS_COST_LIMIT_QUICK_MSG:String  = "デッキコストがチャンネルルールに合わないため、入場できませんでした。";
        CONFIG::LOCALE_KR
        private static const _TRANS_COST_LIMIT_CREATE_MSG:String = "デッキコストがチャンネルルールに合わないため、作成できませんでした。";
        CONFIG::LOCALE_KR
        private static const _TRANS_COST_LIMIT_JOIN_MSG:String   = "デッキコストがチャンネルルールに合わないため、入室できませんでした。";

        CONFIG::LOCALE_FR
        private static const _TRANS_COST_LIMIT_QUICK_MSG:String  = "Le Deck Cost n'allant pas avec les règles du Couloir que vous avez sélectionné, vous ne pouvez y avoir accès.";
        CONFIG::LOCALE_FR
        private static const _TRANS_COST_LIMIT_CREATE_MSG:String = "Le Deck Cost n'allant pas avec les règles du Couloir que vous avez sélectionné, vous ne pouvez pas en créer un nouveau.";
        CONFIG::LOCALE_FR
        private static const _TRANS_COST_LIMIT_JOIN_MSG:String   = "Le Deck Cost n'allant pas avec les règles du Couloir que vous avez sélectionné, vous ne pouvez accéder à cette Salle.";

        CONFIG::LOCALE_ID
        private static const _TRANS_COST_LIMIT_QUICK_MSG:String  = "デッキコストがチャンネルルールに合わないため、入場できませんでした。";
        CONFIG::LOCALE_ID
        private static const _TRANS_COST_LIMIT_CREATE_MSG:String = "デッキコストがチャンネルルールに合わないため、作成できませんでした。";
        CONFIG::LOCALE_ID
        private static const _TRANS_COST_LIMIT_JOIN_MSG:String   = "デッキコストがチャンネルルールに合わないため、入室できませんでした。";

        CONFIG::LOCALE_TH
        private static const _TRANS_COST_LIMIT_QUICK_MSG:String  = "ไม่สามารถเข้าได้เนื่องจาก Deck cost ไม่เข้ากับกฎของ Channel";
        CONFIG::LOCALE_TH
        private static const _TRANS_COST_LIMIT_CREATE_MSG:String = "ไม่สามารถสร้างห้องได้เนื่องจาก Deck cost ไม่เข้ากับกฎของ Channel";
        CONFIG::LOCALE_TH
        private static const _TRANS_COST_LIMIT_JOIN_MSG:String   = "ไม่สามารถเข้าห้องได้เนื่องจาก Deck cost ไม่เข้ากับกฎของ Channel";


        // プレイヤーインスタンス
        private var _player:Player = Player.instance;

        // ロビーサーバー
        private var _lobbyServer:LobbyServer = LobbyServer.instance;

        // BG
        private var _bg:BG = new BG();

        // waiting表示
        private var _gameLobbyView:MatchWaitingView;
        private var _radderLobbyView:RadderWaitingView;
        private var _watchLobbyView:WatchWaitingView;
        private var _viewNormalWaitPanel:Boolean = true;

        // ゲームのコントローラ
        private var _ctrl:DuelCtrl = DuelCtrl.instance;
        // ゲームのコントローラ
        private var _matchCtrl:MatchCtrl = MatchCtrl.instance;

        // 部屋の管理者
        private var _match:Match = Match.instance;

        // デッキ編集インスタンス
        private var _deckEditor:DeckEditor = DeckEditor.instance;

        // 親ステージ
        private var _stage:Sprite;

        // 表示コンテナ
        private var _container:UIComponent = new UIComponent();

        // 現在のデュエル
        private var _duel:Duel = Duel.instance;

        // 現在のステータス
        private var _state:int;

        // タイトル表示
        private var _title:Label = new Label();
        private var _titleJ:Label = new Label();

        // ボタン
        private var _roomJoinButton:RoomJoinButton = new RoomJoinButton(RoomJoinButton.IN);      // 入室時のボタン
        private var _roomOutButton:RoomJoinButton = new RoomJoinButton(RoomJoinButton.OUT);      // 退室時のボタン
        private var _watchJoinButton:RoomJoinButton = new RoomJoinButton(RoomJoinButton.WATCH);  // 観戦時のボタン

        // 部屋作成パネル
        private var _roomCreatePanel:RoomCreatePanel = new RoomCreatePanel();
        // 観戦確認パネル
        private var _watchConfirmPanel:WatchConfirmPanel = new WatchConfirmPanel();

        // エリア表示クラス
        private var _roomArea:RoomArea;
        private var _dataArea:DataArea;
        private var _chatArea:ChatArea;
        private var _avatarArea:AvatarArea;
        private var _channelArea:ChannelArea;

        // ステート定数
        private const _WAITING:int        = 0x000000;              // 待機中
        private const _GAME:int           = 0x000001;              // ゲーム中
        private const _END:int            = 0x000010;              // 終了
        private const _FRIEND:int         = 0x000100;              // フレンドよびだし
        private const _CONNECT:int        = 0x001000;              // 接続待機
        private const _RADDER_CONNECT:int = 0x010000;              // クイックマッチ接続待機

        // 位置定数
        private const _BUTTON_X:int = 25;                   // ボタン位置基本X
        private const _BUTTON_Y:int = 323;                  // ボタン位置基本Y
        private const _BUTTON_OFFSET_Y:int = 73;            // ボタン位置Yのずれ
        private const _BUTTON_SCALE:int = 60;               // ボタンの大きさ(仮)
        private const _TITLE_X:int = 15;
        private const _TITLE_Y:int = 5;
        private const _TITLE_WIDTH:int = 200;
        private const _TITLE_HEIGHT:int = 40;


        /**
         * コンストラクタ
         * @param stage 親ステージ
         */
        public function MatchView(stage:Sprite)
        {
            MatchRoom.clearRoomList();
            _stage = stage;
//            _stage.addChildAt(_container,2);
            _stage.addChild(_container);
            LoadingPanel.create(_stage);
            LoadingPanel.setClickHandler(backChannelHandler);
            _match.initialize();
            _deckEditor.initialize();

            // 仮CPUボタン

            RaidHelpView.instance.isUpdate = true;
        }

        // スレッドのスタート
        override protected  function run():void
        {
            _state = _WAITING;
            next(waitChannelLoad);
        }

        // チャンネル情報の初期化を待つ
        private function  waitChannelLoad():void
        {
//            log.writeLog(log.LV_FATAL, this, "waitChannelLoad", Channel.loaded );

            // チャンネルの情報がロードされていなければ、ロードを待つ
            if (Channel.loaded == false)
            {
                var waitThread:Thread;
                waitThread = Channel.getLoadWaitingThread();
                waitThread.start();
                waitThread.join();
            }
            next(initialize)
        }


        // 部屋情報の初期化
        private function initialize():void
       {
//            log.writeLog(log.LV_FATAL, this, "initialize");
//            log.writeLog(log.LV_FATAL, this, "initialize");
            _bg.alpha = 0.0;
            _title.alpha = 0.0;
            _titleJ.alpha = 0.0;

            _title.x = _TITLE_X;
            _title.y = _TITLE_Y;
            _title.width = _TITLE_WIDTH;
            _title.height = _TITLE_HEIGHT;
            _title.text = "MatchingLobby";
            _title.styleName = "EditTitleLabel";
            _title.filters = [new GlowFilter(0x000000, 1, 2, 2, 16, 1)];

            _title.mouseChildren = false;
            _title.mouseEnabled = false;

            _titleJ.x = _TITLE_X + 140;
            _titleJ.y = _TITLE_Y + 7;
            _titleJ.width = _TITLE_WIDTH;
            _titleJ.height = _TITLE_HEIGHT;
//            _titleJ.text = "対戦ロビー";
            _titleJ.text = _TRANS_LOBBY;
            _titleJ.filters = [new GlowFilter(0xFFFFFF, 1, 2, 2, 16, 1)];

            _titleJ.mouseChildren = false;
            _titleJ.mouseEnabled = false;

            _roomCreatePanel.visible = false;
            _watchConfirmPanel.hidePanel();

            _container.addChild(_title);
            _container.addChild(_titleJ);
            _container.addChild(_roomCreatePanel);
            _container.addChild(_watchConfirmPanel);


            _bg.back.addEventListener(MouseEvent.CLICK, leftDeckClickHandler);
            _bg.next.addEventListener(MouseEvent.CLICK, rightDeckClickHandler);
            _bg.pageBack.addEventListener(MouseEvent.CLICK, leftPageClickHandler);
            _bg.pageNext.addEventListener(MouseEvent.CLICK, rightPageClickHandler);
//            _bg.deckSet.addEventListener(MouseEvent.CLICK, changeClickHandler);
            _bg.chBack.addEventListener(MouseEvent.CLICK, backChannelHandler);

//            _ctrl.setCreateButtons([_bg.quick, _bg.create, _bg.cpuButton]);
            _matchCtrl.setCreateButtons([_bg.create]);
            _matchCtrl.setQuickButtons([_bg.quick]);

            _roomCreatePanel.addEventListener(RoomCreatePanel.CLICK_ROOM_CREATE_BUTTON, clickRoomCreatePanelOkHandler);
            _roomCreatePanel.addEventListener(RoomCreatePanel.CREATE_ROOM, createRoomHandler);
            _roomCreatePanel.addEventListener(RoomCreatePanel.CREATE_ROOM_CANCEL, createRoomCancelHandler);
            _watchConfirmPanel.yesButton.addEventListener(MouseEvent.CLICK, roomWatchStartHandler);
            _watchConfirmPanel.noButton.addEventListener(MouseEvent.CLICK, roomWatchCancelHandler);

            FriendLink.updateBlockList();
            next(registHandlers);
       }


        // ハンドラを登録する
        private function registHandlers():void
        {
//            log.writeLog(log.LV_FATAL, this, "registHandler");
            _roomArea = new RoomArea();
            _dataArea = new DataArea();
            _chatArea = new ChatArea();
            _avatarArea = new AvatarArea();
            _channelArea = new ChannelArea();

//            log.writeLog(log.LV_FATAL, this, "regist handle");
            _bg.chatButton.addEventListener(MouseEvent.CLICK, pushChatButtonHandler);
            _bg.quick.addEventListener(MouseEvent.CLICK, pushQuickStartButtonHandler);
            _bg.create.addEventListener(MouseEvent.CLICK, pushCreateRoomButtonHandler);

            _avatarArea.exitButton.addEventListener(MouseEvent.CLICK, pushExitButton);

            _roomJoinButton.addEventListener(MouseEvent.CLICK, pushRoomJoinButtonHandler);
            _roomOutButton.addEventListener(MouseEvent.CLICK, pushRoomOutButtonHandler);
            _watchJoinButton.addEventListener(MouseEvent.CLICK, pushRoomWatchButtonHandler);

            _match.addEventListener(MatchEvent.CREATE_SUCCESS, connectedHander);
            _match.addEventListener(MatchEvent.DELETE_ROOM, roomDeleteHandler);
            _match.addEventListener(MatchEvent.EXIT_ROOM, roomExitHandler);
            _match.addEventListener(Match.ROOM_CLICK, roomClickHandler);
            _match.addEventListener(Match.LOADING, loadingChannelHandler);

            // レイドヘルプイベント
            GlobalChatCtrl.instance.addEventListener(RaidHelpEvent.ACCEPT,helpAcceptHandler);

            next(show);
        }

        // 配置オブジェの表示
        private function show():void
        {
            //log.writeLog(log.LV_DEBUG, this, "show !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
            _ctrl.playMatchBGM();
//            log.writeLog(log.LV_FATAL, this, "bg",_bg.quick, _bg.create,_bg.cpuButton);
            _bg.quick.visible = false;
            _bg.create.visible = false;

            var pExec:ParallelExecutor = new ParallelExecutor();
            pExec.addThread(_bg.getShowThread(_container,0));
            pExec.addThread(_chatArea.getShowThread(_container,1));

            pExec.addThread(_dataArea.getShowThread(_container,2));
            pExec.addThread(_avatarArea.getShowThread(_container,3));
            pExec.addThread(_roomArea.getShowThread(_container,4));
            pExec.addThread(_channelArea.getShowThread(_container,5));

            pExec.addThread(new BeTweenAS3Thread(_bg, {alpha:1.0}, null, 0.8 / Unlight.SPEED, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,true));
            pExec.addThread(new BeTweenAS3Thread(_title, {alpha:1.0}, null, 0.8 / Unlight.SPEED, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,true));
            pExec.addThread(new BeTweenAS3Thread(_titleJ, {alpha:1.0}, null, 0.8 / Unlight.SPEED, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,true));
            pExec.start();
            pExec.join();

            // チャンネル選択済みならチャンネルを選択する
            log.writeLog(log.LV_FATAL, this, "Channel no is", Channel.current);

            if(_ctrl.connected && (Channel.current != -1))
            {
                _matchCtrl.matchListInfoUpdate();
                _bg.setChannel(Channel.current);
                _channelArea.visible = false;
                if (Channel.list[Channel.current].isRadder)
                {
                    _bg.quick.visible = true;
                }else{
                    _bg.create.visible = true;
                }

                //_matchCtrl.achievementClearCheck();
                // 画面遷移しても問題ないよう、LobbyCtrlでチェック
                LobbyCtrl.instance.achievementClearCheck(false);
            }

            // デッキの設定
            _bg.deckNum = _deckEditor.deckNum;
            _bg.currentNum = _deckEditor.currentIndex;
            deckSelectButtonChangeEnabled(true);
            next(initButton);
        }

        // ボタンの初期化
        private function initButton():void
        {
            _roomJoinButton.visible = false;
            _roomOutButton.visible = false;
            _watchJoinButton.visible = false;
            _container.addChildAt(_roomJoinButton, 3);
            //_container.addChildAt(_roomOutButton, 3);
            _container.addChildAt(_watchJoinButton, 3);


            // チャンネル選択済みならチャンネルを選択する
            if(Channel.current != -1)
            {
                next(joining);
            }
            else
            {
                next(waiting);
            }
        }

        // チャンネルに入る
        private function joining():void
        {
            _channelArea.joinChannel(Channel.current);
            next(waiting);
        }

        // 待つ
        private function waiting():void
        {
            if (_player.state == Player.STATE_LOGOUT)
            {
                next(hide);
            }else{
                // ステートによって切り替える
                switch(_state)
                {
                case _GAME:
                    next(game);
                    break;
                case _END:
                    next(hide);
                    break;
                case _FRIEND:
                    next(friend);
                    break;
                case _CONNECT:
                    next(connect);
                    break;
                case _RADDER_CONNECT:
                    next(radderConnect);
                    break;
                default:
                    next(waiting);
                }

            }
        }

        // 接続待機中
        private function connect():void
        {
//            _roomCreatePanel.visible = false;
//            log.writeLog(log.LV_FATAL, this, "connect");
            setMouseEnabled(false);

            if ( _viewNormalWaitPanel ) {
                _gameLobbyView = new MatchWaitingView(_stage, _match.currentRoomId);
                _gameLobbyView.start();
                _gameLobbyView.join();
            } else {
                _watchLobbyView = new WatchWaitingView(_stage, _match.currentRoomId);
                _watchLobbyView.start();
                _watchLobbyView.join();
            }

            next(connection);
        }

        // 接続待機中
        private function radderConnect():void
        {
            setMouseEnabled(false);

            if ( _viewNormalWaitPanel ) {
                _radderLobbyView = new RadderWaitingView(_stage, _match.currentRoomId);
                _radderLobbyView.start();
                _radderLobbyView.join();
            } else {
                _watchLobbyView = new WatchWaitingView(_stage, _match.currentRoomId);
                _watchLobbyView.start();
                _watchLobbyView.join();
            }

            next(connection);
        }

        // 接続or部屋消去
        private function connection():void
        {
            log.writeLog (log.LV_INFO,this,"connection.",(_duel.state == Duel.START));
            if (_duel.state == Duel.START)
            {
                // log.writeLog (log.LV_INFO,this,"duel started");
                _state = _GAME;
                _ctrl.state = DuelCtrl.GAME_STAGE;
                _ctrl.stageNo = (MatchRoom.list[_match.currentRoomId] != null) ? MatchRoom.list[_match.currentRoomId].stage : 0;
            }
            else
            {
                // 部屋から抜ける
                _match.exitRoom();
                _state = _WAITING;
                _ctrl.state = DuelCtrl.WAITING;
                // WatchCtrl.instance.watchFinish();
                // Duel.instance.isWatch = false;
                _roomJoinButton.visible = false;
                _watchJoinButton.visible = false;
                setMouseEnabled(true);
                deckSelectButtonChangeEnabled(true);
            }

//            _roomCreatePanel.visible = false;
            _roomOutButton.visible = false;
            next(waiting);
        }





        // ゲームに移行
        private function game():void
        {
//            log.writeLog(log.LV_FATAL, this, "game");
            _ctrl.stopMatchBGM();
//            Transition.instance.setTransionImage(_container, _stage);
            // 表示を全て消す
            var pExec:ParallelExecutor = new ParallelExecutor();
            pExec.addThread(new BeTweenAS3Thread(_bg, {alpha:0.0}, null, 0.8 / Unlight.SPEED, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,false));
            pExec.addThread(new BeTweenAS3Thread(_roomJoinButton, {alpha:0.0}, null, 0.8 / Unlight.SPEED, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,false));
            pExec.addThread(new BeTweenAS3Thread(_roomOutButton, {alpha:0.0}, null, 0.8 / Unlight.SPEED, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,false));
            pExec.addThread(new BeTweenAS3Thread(_watchJoinButton, {alpha:0.0}, null, 0.8 / Unlight.SPEED, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,false));
            pExec.addThread(new BeTweenAS3Thread(_title, {alpha:0.0}, null, 0.8 / Unlight.SPEED, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,false));
            pExec.addThread(new BeTweenAS3Thread(_titleJ, {alpha:0.0}, null, 0.8 / Unlight.SPEED, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,false));
            pExec.addThread(_chatArea.getHideThread());
            pExec.addThread(_avatarArea.getHideThread());
            pExec.addThread(_roomArea.getHideThread());
            pExec.addThread(_channelArea.getHideThread());
            pExec.addThread(_dataArea.getHideThread());
            pExec.start();
            pExec.join();
//            log.writeLog(log.LV_FATAL, this, "game");
            next(exit);
        }

        // フレンド（何をするかは未定）
        private function friend():void
        {
            next(friend);
        }

        // ビューのマウスイベントを設定する
        private function setMouseEnabled(s:Boolean):void
        {
            _bg.mouseEnabled = s;
            _bg.mouseChildren = s;
            _avatarArea.mouseEnabled = s;
            _avatarArea.mouseChildren = s;
            _channelArea.mouseEnabled = s;
            _channelArea.mouseChildren = s;
            _roomArea.mouseEnabled = s;
            _roomArea.mouseChildren = s
            _chatArea.mouseEnabled = s;
            _chatArea.mouseChildren = s;

            RaidHelpView.instance.isUpdate = s;
        }

        private function joinButtonViewCheck():Boolean
        {
            return (_state != _CONNECT && _state != _RADDER_CONNECT && _state != _GAME );
        }
        // 部屋がクリックされたときのハンドラ
        private function roomClickHandler(e:Event):void
        {
//            log.writeLog(log.LV_INFO, this, "room click handler !!!");
            SE.playChannelClickSE();
//            if(MatchRoom.list[_match.currentRoomId] && MatchRoom.list[_match.currentRoomId].length < 2)
            if(MatchRoom.list[_match.currentRoomId] && joinButtonViewCheck() )
            {
//                _roomJoinButton.visible = true;
                if (MatchRoom.list[_match.currentRoomId].length < 2) {
                    _roomJoinButton.visible = true;
                    _watchJoinButton.visible = false;
                } else {
                    _roomJoinButton.visible = false;
                    if (Channel.list[Channel.current].watchMode == Channel.WATCH_MODE_ON) {
                        _watchJoinButton.visible = true;
                    }
                }
            }
            else
            {
                _roomJoinButton.visible = false;
                _watchJoinButton.visible = false;
//                _roomJoinButton.visible = true;
            }
        }

        // 終了
        private function pushExitButton(e:MouseEvent):void
        {
            SE.playClick();
 //            if (_ctrl.serverState == _ctrl.CONNECT_AUTHED && _state != _CONNECT)
//             {
//                Channel.exitChannel(0);
            _ctrl.exitChannelServerDisconnect();
            ChatCtrl.instance.exitChannelServerDisconnect();
            MatchCtrl.instance.exitChannelServerDisconnect();
            WatchCtrl.instance.exitChannelServerDisconnect();
            MatchRoom.clearRoomList();

            _player.state = Player.STATE_LOBBY;
            _ctrl.exit();
            ChatCtrl.instance.exit();
            _ctrl.state = DuelCtrl.EXIT;
            WatchCtrl.instance.state = WatchCtrl.EXIT;
            _state = _END;
//             }

//            log.writeLog(log.LV_INFO, this, "push exit");
        }

        // ウェイトパネルのキャンセルボタンのハンドラ
        private function quickmatchWaitCancelHandler():void
        {
            log.writeLog(log.LV_INFO, this, "[quickmatchWaitCancelHandler]");
//             _matchCtrl.deleteQuickmatchList();
//             WaitingPanel.hide();
        }

        private function deckSelectButtonChangeEnabled(enable:Boolean):void
        {
            _bg.back.mouseEnabled = enable;
            _bg.next.mouseEnabled = enable;
        }

        // 部屋作成（クイックスタート）
        private function pushQuickStartButtonHandler(e:MouseEvent):void
        {
//             SE.playClick();
            // 先にコスト制限チェック
            deckSelectButtonChangeEnabled(false);
            log.writeLog(log.LV_DEBUG, this, "push Quick Start",Player.instance.avatar.currentDeckCost);
            log.writeLog(log.LV_DEBUG, this, "push Quick Start",Channel.list[Channel.current].costLimitCheck(Player.instance.avatar.currentDeckCost));
            log.writeLog(log.LV_DEBUG, this, "push Quick Start",Channel.list[Channel.current].isRadder);
            if ( Channel.list[Channel.current].costLimitCheck(Player.instance.avatar.currentDeckCost)&&(Channel.list[Channel.current].isRadder) )
            {
                var rule:int = (Player.instance.avatar.getCurrentDeck().length == 3) ? 1 : 0;
                _matchCtrl.addQuickmatchList(rule);
                _ctrl.state = DuelCtrl.GAME_STAGE;
                _state = _RADDER_CONNECT;
                _roomJoinButton.visible = false;
                _watchJoinButton.visible = false;
                _bg.quick.removeEventListener(MouseEvent.CLICK, pushQuickStartButtonHandler);
                new WaitThread(3000,_bg.quick.addEventListener,[MouseEvent.CLICK, pushQuickStartButtonHandler] ).start();
                // if(_state != _CONNECT)
                // {
                //     var rule:int = (Player.instance.avatar.getCurrentDeck().length == 3) ? 1 : 0;
                //     _matchCtrl.addQuickmatchList(rule);
                //     _ctrl.state = DuelCtrl.GAME_STAGE;
                //     _state = _RADDER_CONNECT;
                //     _roomJoinButton.visible = false;
                // }
            } else {
                Alerter.showWithSize(_TRANS_COST_LIMIT_QUICK_MSG,_TRANS_ALERT)
                    deckSelectButtonChangeEnabled(true);
            }
            _viewNormalWaitPanel = true;
            log.writeLog(log.LV_INFO, this, "push Quick Start");
        }

        public function CheckCost():Boolean
        {
            _viewNormalWaitPanel = true;
            if (Channel.list[Channel.current].isRadder)
            {
                if ( Channel.list[Channel.current].costLimitCheck(Player.instance.avatar.currentDeckCost))
                {
                    return true;
                }
                else
                {
                    Alerter.showWithSize(_TRANS_COST_LIMIT_QUICK_MSG,_TRANS_ALERT)
                        deckSelectButtonChangeEnabled(true);

                    return false;
                }
            }
            return true;
        }

        public function CheckRule():Boolean
        {
            if (Channel.list[Channel.current].isRadder)
            {
                return Player.instance.avatar.getCurrentDeck().length == 3
            }
            else
            {
                return (_roomCreatePanel.duelRule == 0 && Player.instance.avatar.getCurrentDeck().length == 1) || (_roomCreatePanel.duelRule == 1 && Player.instance.avatar.getCurrentDeck().length == 3);
            }
        }

        // 部屋作成
        private function pushCreateRoomButtonHandler(e:MouseEvent):void
        {
//             SE.playClick();
            // log.writeLog(log.LV_INFO, this, "push create room",_state);
            // 先にコスト制限チェック
            deckSelectButtonChangeEnabled(false);
            if ( Channel.list[Channel.current].costLimitCheck(Player.instance.avatar.currentDeckCost) )
            {
                if(_state != _CONNECT)
                {
                    setMouseEnabled(false);
                    _roomCreatePanel.visible = true;
                }
            } else {
                Alerter.showWithSize(_TRANS_COST_LIMIT_CREATE_MSG,_TRANS_ALERT);
                deckSelectButtonChangeEnabled(true);
            }
            _viewNormalWaitPanel = true;

//            log.writeLog(log.LV_INFO, this, "push create room");
        }

        // 部屋作成
        private function createRoomHandler(e:Event):void
        {
            _roomCreatePanel.visible = false;
            setMouseEnabled(true);

//             SE.playClick();
            if(_state != _CONNECT)
            {
//                log.writeLog(log.LV_INFO, this, "room status", _roomCreatePanel.roomName, _roomCreatePanel.duelStage, _roomCreatePanel.duelRule);
                _match.createRoom(_roomCreatePanel.roomName, _roomCreatePanel.duelStage, _roomCreatePanel.duelRule);
                _roomJoinButton.visible = false;
                _roomOutButton.visible = false;
                _watchJoinButton.visible = false;
            }
            deckSelectButtonChangeEnabled(true);
//            log.writeLog(log.LV_INFO, this, "create room");
        }

        private function clickRoomCreatePanelOkHandler(e:Event):void
        {
            if (CheckCost() && CheckRule())
            {
                _roomCreatePanel.ValidText();
            }
            else
            {
                Alerter.showWithSize("チャンネルルールに合わないため、作成できませんでした。", "情報");
            }
        }

        // 部屋作成
        private function createRoomCancelHandler(e:Event):void
        {
            _roomCreatePanel.visible = false;
            setMouseEnabled(true);
            deckSelectButtonChangeEnabled(true);
//            log.writeLog(log.LV_INFO, this, "create room cancel");
        }

        // 観戦ボタンクリック
        private function pushRoomWatchButtonHandler(e:MouseEvent):void
        {
            // log.writeLog(log.LV_INFO, this, "pushRoomWatchButtonHandler", (_state != _CONNECT));
            if(_state != _CONNECT)
            {
                setMouseEnabled(false);
                _watchConfirmPanel.showPanel(_match.currentRoomId);
            }
        }

        // 観戦開始
        private function roomWatchStartHandler(e:Event):void
        {
            // log.writeLog(log.LV_INFO, this, "roomWatchStartHandler");
            // Duel中の場合のみ
            if(MatchRoom.list[_match.currentRoomId] && MatchRoom.list[_match.currentRoomId].length >= 2) {
                log.writeLog(log.LV_INFO, this, "roomWatchStartHandler 1");
                _watchConfirmPanel.hidePanel();
                WatchCtrl.instance.watchStart(_match.currentRoomId);
                Duel.instance.isWatch = true;
                _ctrl.state = DuelCtrl.GAME_STAGE;
                WatchCtrl.instance.state = WatchCtrl.GAME_STAGE;
                _state = _CONNECT;
                _roomJoinButton.visible = false;
                _watchJoinButton.visible = false;
                _viewNormalWaitPanel = false;
            }
        }

        // 観戦キャンセル
        private function roomWatchCancelHandler(e:Event):void
        {
            // log.writeLog(log.LV_INFO, this, "roomWatchCancelHandler");
            _watchConfirmPanel.hidePanel();
            setMouseEnabled(true);
        }

        // チャンネルをロード中
        private function loadingChannelHandler(e:Event):void
        {
            _bg.setChannel(_match.currentChannelId);
        }

//         // ゲームのクイックスタート（オートマッチング）
//         private function pushQuickStartButtonHandler(e:MouseEvent):void
//         {
// //            log.writeLog(log.LV_INFO, this, "push quick start");
//             SE.playClick();

//             if(_state != _CONNECT)
//             {
//                 for(var key:String in MatchRoom.list)
//                 {
//                     if(MatchRoom.list[key] != null && MatchRoom.list[key].length < 2)
//                     {
//                         _match.currentRoomId = key;
//                         _match.joinRoom(MatchRoom.list[key].id);
//                         _state = _CONNECT;
//                         _roomJoinButton.visible = false;
//                     }
//                 }
//                 pushCreateRoomButtonHandler(e);
// //                _ctrl.state = DuelCtrl.GAME_STAGE;
//             }
//         }


        // 入室
        private function pushRoomJoinButtonHandler(e:MouseEvent):void
        {
            // 現在APが足りてるかをチェック
//             if (MatchRoom.list[_match.currentRoomId] && Const.DUEL_AP[MatchRoom.list[_match.currentRoomId].rule] <= Player.instance.avatar.energy)
//             {
            SE.playClick();
//                log.writeLog(log.LV_FATAL, this, "Consts+++",Const.DUEL_NUM[MatchRoom.list[_match.currentRoomId].rule], Player.instance.avatar.getCurrentDeck().length);
            if(MatchRoom.list[_match.currentRoomId] && MatchRoom.list[_match.currentRoomId].length < 2) {
            // Duelが始まっていない場合の処理
                // 先にコスト制限チェック
                if ( Channel.list[Channel.current].costLimitCheck(Player.instance.avatar.currentDeckCost) )
                {
                    if (Const.DUEL_NUM[MatchRoom.list[_match.currentRoomId].rule]== Player.instance.avatar.getCurrentDeck().length)
                    {
                        if(_state != _CONNECT)
                        {
                            _player.joined = true;
                            // 無効な部屋番号を判定
                            if(MatchRoom.list[_match.currentRoomId].length < 2)
                            {
                                MatchCtrl.instance.joinRoom(_match.currentRoomId);
                                _match.joinRoom(_match.currentRoomId);
                                Duel.instance.isWatch = false;
                                _ctrl.state = DuelCtrl.GAME_STAGE;
                                _state = _CONNECT;
                                _roomJoinButton.visible = false;
                                _watchJoinButton.visible = false;
                                _viewNormalWaitPanel = true;
                            }
                        }
                    }else{
//                    Alerter.showWithSize("デッキ枚数が異なります","警告")
                        Alerter.showWithSize(_TRANS_MSG1,_TRANS_ALERT);
                    }
                } else {
                    Alerter.showWithSize(_TRANS_COST_LIMIT_JOIN_MSG,_TRANS_ALERT);
                }
            }
//             }else{
// //                Alerter.showWithSize("APが足りません","警告")
//                 Alerter.showWithSize(_TRANS_MSG2,_TRANS_ALERT)
//             }
//            log.writeLog(log.LV_INFO, this, "push join room");
        }

        // 退室
        private function pushRoomOutButtonHandler(e:MouseEvent):void
        {
            _match.connectChancel();
//            log.writeLog(log.LV_INFO, this, "push out room");
        }

//         // カレントデッキを変更
//         private function changeClickHandler(e:MouseEvent):void
//         {
//             _avatarArea.changeClick();
//         }

        // 左のページをクリック
        private function leftPageClickHandler(e:MouseEvent):void
        {
            _roomArea.prevPage();
        }

        // 右のページをクリック
        private function rightPageClickHandler(e:MouseEvent):void
        {
            _roomArea.nextPage();
        }

        // 左のデッキをクリック
        private function leftDeckClickHandler(e:MouseEvent):void
        {
            SE.playClick();
            _avatarArea.leftDeckClick();
            _bg.currentNum = _deckEditor.selectIndex;
            _avatarArea.changeClick();

        }

        // 右のデッキをクリック
        private function rightDeckClickHandler(e:MouseEvent):void
        {
            SE.playClick();
            _avatarArea.rightDeckClick();
            _bg.currentNum = _deckEditor.selectIndex;
            _avatarArea.changeClick();
        }

        private function pushChatButtonHandler(e:MouseEvent):void
        {
            _chatArea.sendText();
        }

        // チャンネルに戻る
        private function backChannelHandler(e:MouseEvent):void
        {
            log.writeLog(log.LV_INFO, this, "backchannelhandler");
            _chatArea.resetSelector();
            _channelArea.visible = true;

            // 部屋作成、クイックスタートボタンを非表示
            _matchCtrl.createButtonsEnable(false);
            _matchCtrl.quickButtonsEnable(false);

            _ctrl.exitChannelServerDisconnect();
            ChatCtrl.instance.exitChannelServerDisconnect();
            MatchCtrl.instance.exitChannelServerDisconnect();
            WatchCtrl.instance.exitChannelServerDisconnect();

            _dataArea.visible = false;
            _roomArea.visible = false;
            _roomJoinButton.visible = false;
            _roomOutButton.visible = false;
            _watchJoinButton.visible = false;
            FriendLink.updateBlockList();
            LoadingPanel.offLoading();
        }

        // フレンドへ移行
        private function pushFriendButton(e:MouseEvent):void
        {
            //_state = _FRIEND;
//            log.writeLog(log.LV_INFO, this, "push friend");
        }

        // 接続状態にするハンドラ
        private function connectedHander(e:MatchEvent):void
        {
//            log.writeLog(log.LV_INFO, this, "id", e.id);
            if(e.id != "")
            {
                _player.joined = false;
                //_roomOutButton.visible = true;
//                _ctrl.state = DuelCtrl.GAME_STAGE;
                _state = _CONNECT;
            }
        }

        // ルームが消された時のハンドラ
        private function roomDeleteHandler(e:MatchEvent):void
        {
            // log.writeLog(log.LV_FATAL, this, "*********** roomDeleteHandler event.id, panel.id", e.id, _watchConfirmPanel.selectRoomId);
            if (e.id == _watchConfirmPanel.selectRoomId) {
                _watchConfirmPanel.hidePanel();
                setMouseEnabled(true);
            }
        }
        // ルームが消された時のハンドラ
        private function roomExitHandler(e:MatchEvent):void
        {
            _roomJoinButton.visible = false;
            _roomOutButton.visible = false;
            _watchJoinButton.visible = false;
        }

        // レイドヘルプハンドラ
        private function helpAcceptHandler(e:RaidHelpEvent):void
        {
            SE.playClick();
 //            if (_ctrl.serverState == _ctrl.CONNECT_AUTHED && _state != _CONNECT)
//             {
//                Channel.exitChannel(0);
            _ctrl.exitChannelServerDisconnect();
            ChatCtrl.instance.exitChannelServerDisconnect();
            MatchCtrl.instance.exitChannelServerDisconnect();
            WatchCtrl.instance.exitChannelServerDisconnect();
            MatchRoom.clearRoomList();

            _player.state = Player.STATE_LOBBY;
            _ctrl.exit();
            ChatCtrl.instance.exit();
            _ctrl.state = DuelCtrl.EXIT;
            WatchCtrl.instance.state = WatchCtrl.EXIT;
            _state = _END;
//             }

//            log.writeLog(log.LV_INFO, this, "push exit");
        }

        // スレッドを隠す
        private function hide():void
        {
//            log.writeLog(log.LV_FATAL, this, "hide");
            _ctrl.stopMatchBGM();
            // 表示を全て消す
            var pExec:ParallelExecutor = new ParallelExecutor();
            pExec.addThread(new BeTweenAS3Thread(_bg, {alpha:0.0}, null, 0.8 / Unlight.SPEED, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,false));
            pExec.addThread(new BeTweenAS3Thread(_roomJoinButton, {alpha:0.0}, null, 0.8 / Unlight.SPEED, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,false));
            pExec.addThread(new BeTweenAS3Thread(_roomOutButton, {alpha:0.0}, null, 0.8 / Unlight.SPEED, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,false));
            pExec.addThread(new BeTweenAS3Thread(_watchJoinButton, {alpha:0.0}, null, 0.8 / Unlight.SPEED, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,false));
            pExec.addThread(new BeTweenAS3Thread(_title, {alpha:0.0}, null, 0.8 / Unlight.SPEED, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,false));
            pExec.addThread(new BeTweenAS3Thread(_titleJ, {alpha:0.0}, null, 0.8 / Unlight.SPEED, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,false));
            pExec.addThread(_chatArea.getHideThread());
            pExec.addThread(_avatarArea.getHideThread());
            pExec.addThread(_roomArea.getHideThread());
            pExec.addThread(_channelArea.getHideThread());
            pExec.addThread(_dataArea.getHideThread());
            pExec.start();
            pExec.join();

            next(exit);
        }

        // 終了
        private function exit():void
        {
            // イベントを消去する
//            log.writeLog(log.LV_FATAL, this, "exi");
            _bg.back.removeEventListener(MouseEvent.CLICK, leftDeckClickHandler);
            _bg.next.removeEventListener(MouseEvent.CLICK, rightDeckClickHandler);
            _bg.pageBack.removeEventListener(MouseEvent.CLICK, leftPageClickHandler);
            _bg.pageNext.removeEventListener(MouseEvent.CLICK, rightPageClickHandler);
//            _bg.deckSet.removeEventListener(MouseEvent.CLICK, changeClickHandler);
            _bg.chBack.removeEventListener(MouseEvent.CLICK, backChannelHandler);
            _bg.chatButton.removeEventListener(MouseEvent.CLICK, pushChatButtonHandler);
            _bg.quick.removeEventListener(MouseEvent.CLICK, pushQuickStartButtonHandler);
            _bg.create.removeEventListener(MouseEvent.CLICK, pushCreateRoomButtonHandler);
            _avatarArea.exitButton.removeEventListener(MouseEvent.CLICK, pushExitButton);
            _roomCreatePanel.removeEventListener(RoomCreatePanel.CREATE_ROOM, createRoomHandler);
            _roomCreatePanel.removeEventListener(RoomCreatePanel.CREATE_ROOM_CANCEL, createRoomCancelHandler);
            _watchConfirmPanel.yesButton.removeEventListener(MouseEvent.CLICK,roomWatchStartHandler);
            _watchConfirmPanel.noButton.removeEventListener(MouseEvent.CLICK,roomWatchCancelHandler);
            _roomJoinButton.removeEventListener(MouseEvent.CLICK, pushRoomJoinButtonHandler);
            _roomOutButton.removeEventListener(MouseEvent.CLICK, pushRoomOutButtonHandler);
            _watchJoinButton.removeEventListener(MouseEvent.CLICK, pushRoomWatchButtonHandler);
            _match.removeEventListener(MatchEvent.CREATE_SUCCESS, connectedHander);
            _match.removeEventListener(MatchEvent.DELETE_ROOM, roomDeleteHandler);
            _match.removeEventListener(MatchEvent.EXIT_ROOM, roomExitHandler);
            _match.removeEventListener(Match.ROOM_CLICK, roomClickHandler);
            _match.removeEventListener(Match.LOADING, loadingChannelHandler);

            // レイドヘルプイベント
            GlobalChatCtrl.instance.removeEventListener(RaidHelpEvent.ACCEPT,helpAcceptHandler);

            _match.finalize();
            _deckEditor.finalize();
            _matchCtrl.removeCreateButtons();
            _matchCtrl.removeQuickButtons();
//            log.writeLog(log.LV_INFO, this, "match exit");
        }

        // 終了関数
        override protected function finalize():void
        {
//            Unlight.GCW.watch(this);
            log.writeLog(log.LV_FATAL, this, "finalize match view");
            RemoveChild.all(_container);
            _stage.removeChild(_container);
            _bg =null;
            _roomArea = null;
            _dataArea = null;
            _chatArea = null;
            _avatarArea = null;
            _channelArea = null;
            _roomJoinButton = null;
            _roomOutButton = null;
            _watchJoinButton = null;
            LoadingPanel.final();

        // ステート定数

        }

        // カレントキャラカードIDを見つける関数
        private function get currentCharaCardId():int
        {
            var avatar:Avatar = _player.avatar;
            return CharaCardDeck.decks[avatar.currentDeck].charaCardInventories[0].charaCard.id | 1
        }

   }

}
